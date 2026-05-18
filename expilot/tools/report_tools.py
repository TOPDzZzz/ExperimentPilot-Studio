from pathlib import Path
from datetime import datetime
from html import escape


def generate_markdown_report(title: str, content: str, output_path: str = None) -> str:
    """Generate a Markdown report file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"outputs/report_{timestamp}.md"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    report = f"""# {title}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{content}
"""
    Path(output_path).write_text(report, encoding="utf-8")
    return f"Report generated: {output_path}"


def generate_html_report(title: str, content: str, output_path: str = None) -> str:
    """Generate an HTML report file."""
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"outputs/report_{timestamp}.html"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    safe_title = escape(title)
    safe_content = escape(content).replace("\n", "<br>")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
        .container {{ background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #c96442; padding-bottom: 0.5rem; }}
        .meta {{ color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; }}
        pre {{ background: #f8f8f8; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{safe_title}</h1>
        <p class="meta">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <div class="content">
            {safe_content}
        </div>
    </div>
</body>
</html>"""
    Path(output_path).write_text(html, encoding="utf-8")
    return f"HTML report generated: {output_path}"


def save_text_output(content: str, filename: str = None) -> str:
    """Save text content to outputs directory."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestamp}.txt"

    output_path = Path("outputs") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return f"Output saved: {output_path}"
