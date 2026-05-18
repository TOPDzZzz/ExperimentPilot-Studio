from pathlib import Path
from typing import List

WORKSPACE = Path("workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)


def _safe_path(path: str) -> Path:
    """Resolve path and prevent escaping workspace."""
    target = (WORKSPACE / path).resolve()
    workspace = WORKSPACE.resolve()

    if not str(target).startswith(str(workspace)):
        raise ValueError("Access outside workspace is not allowed")

    return target


def list_dir(path: str = ".") -> str:
    """List files and folders in workspace."""
    target = _safe_path(path)
    if not target.exists():
        return f"Path not found: {path}"
    if not target.is_dir():
        return f"Not a directory: {path}"

    items: List[str] = []
    for child in sorted(target.iterdir()):
        prefix = "[DIR]" if child.is_dir() else "[FILE]"
        items.append(f"{prefix} {child.name}")

    return "\n".join(items) if items else "Directory is empty."


def read_file(path: str, max_chars: int = 8000) -> str:
    """Read file content from workspace."""
    target = _safe_path(path)
    if not target.exists():
        return f"File not found: {path}"
    if not target.is_file():
        return f"Not a file: {path}"

    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[TRUNCATED]"
    return text


def write_file(path: str, content: str) -> str:
    """Write content to a file in workspace."""
    target = _safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"File written: {path}"


def search_files(keyword: str, path: str = ".", max_results: int = 20) -> str:
    """Search for files by keyword in workspace."""
    target = _safe_path(path)
    if not target.exists() or not target.is_dir():
        return f"Invalid directory: {path}"

    results = []
    for file in target.rglob("*"):
        if file.is_file():
            try:
                text = file.read_text(encoding="utf-8", errors="ignore")
                if keyword.lower() in text.lower() or keyword.lower() in file.name.lower():
                    results.append(str(file.relative_to(WORKSPACE)))
            except Exception:
                continue

        if len(results) >= max_results:
            break

    return "\n".join(results) if results else "No matching files found."
