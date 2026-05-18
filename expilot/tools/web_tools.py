import urllib.request
import urllib.parse
import json
from pathlib import Path

WORKSPACE = Path("workspace").resolve()


def _safe_path(path: str) -> Path:
    """Resolve path and prevent escaping workspace."""
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise ValueError("Access outside workspace is not allowed")
    return target


def fetch_url(url: str, max_chars: int = 5000) -> str:
    """Fetch content from a URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ExperimentPilot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[TRUNCATED]"
            return content
    except Exception as e:
        return f"Failed to fetch URL: {e}"


def search_web(query: str, num_results: int = 5) -> str:
    """Search the web using DuckDuckGo Lite (no API key required)."""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"
        req = urllib.request.Request(url, headers={"User-Agent": "ExperimentPilot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        results = []
        import re
        links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="result-link"[^>]*>([^<]+)</a>', html)
        for i, (link, title) in enumerate(links[:num_results]):
            results.append(f"{i+1}. {title.strip()}\n   {link}")

        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


def download_file(url: str, save_path: str) -> str:
    """Download a file from URL to workspace."""
    try:
        target = _safe_path(save_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "ExperimentPilot/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            target.write_bytes(resp.read())
        return f"File downloaded: {save_path}"
    except Exception as e:
        return f"Download failed: {e}"
