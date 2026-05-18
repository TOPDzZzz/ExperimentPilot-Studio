from pathlib import Path

WORKSPACE = Path("workspace").resolve()
CODE_SUFFIXES = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".html", ".css"}


def _safe_path(path: str) -> Path:
    """Resolve path and prevent escaping workspace."""
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise ValueError("Access outside workspace is not allowed")
    return target


def scan_code_project(root: str = "workspace") -> str:
    """Scan code project structure within workspace."""
    root_path = _safe_path(root)
    if not root_path.exists():
        return f"Path not found: {root}"
    files = [str(p.relative_to(root_path)) for p in root_path.rglob("*") if p.is_file() and p.suffix in CODE_SUFFIXES]
    return "\n".join(files) if files else "No code files found."


def read_code_file(path: str) -> str:
    """Read a code file for analysis within workspace."""
    target = _safe_path(path)
    if not target.exists():
        return f"File not found: {path}"
    return target.read_text(encoding="utf-8", errors="ignore")
