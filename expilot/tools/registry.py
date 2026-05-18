from typing import Any, Callable, Dict
from expilot.tools.file_tools import list_dir, read_file, write_file, search_files
from expilot.tools.shell_tools import run_shell
from expilot.tools.code_tools import scan_code_project, read_code_file
from expilot.tools.data_tools import analyze_csv, analyze_excel
from expilot.tools.ml_tools import summarize_json_metrics, compare_experiment_results, generate_experiment_report
from expilot.tools.report_tools import generate_markdown_report, generate_html_report, save_text_output
from expilot.tools.web_tools import fetch_url, search_web, download_file

TOOLS: Dict[str, Callable[..., str]] = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
    "run_shell": run_shell,
    "scan_code_project": scan_code_project,
    "read_code_file": read_code_file,
    "analyze_csv": analyze_csv,
    "analyze_excel": analyze_excel,
    "summarize_json_metrics": summarize_json_metrics,
    "compare_experiment_results": compare_experiment_results,
    "generate_experiment_report": generate_experiment_report,
    "generate_markdown_report": generate_markdown_report,
    "generate_html_report": generate_html_report,
    "save_text_output": save_text_output,
    "fetch_url": fetch_url,
    "search_web": search_web,
    "download_file": download_file,
}

TOOL_DESCRIPTIONS = {
    "list_dir": "List files and folders. Params: {\"path\": \"relative path, default '.'\"}",
    "read_file": "Read file content. Params: {\"path\": \"relative path (REQUIRED)\", \"max_chars\": 8000}",
    "write_file": "Write content to file. Params: {\"path\": \"relative path (REQUIRED)\", \"content\": \"text (REQUIRED)\"}",
    "search_files": "Search files by keyword. Params: {\"keyword\": \"search term (REQUIRED)\", \"path\": \".\"}",
    "run_shell": "Execute shell command. Params: {\"command\": \"shell command (REQUIRED)\"}",
    "scan_code_project": "Scan code project. Params: {\"root\": \"root path, default 'workspace'\"}",
    "read_code_file": "Read code file. Params: {\"path\": \"relative path (REQUIRED)\"}",
    "analyze_csv": "Analyze CSV stats. Params: {\"path\": \"relative path (REQUIRED)\"}",
    "analyze_excel": "Analyze Excel stats. Params: {\"path\": \"relative path (REQUIRED)\"}",
    "summarize_json_metrics": "Summarize JSON metrics. Params: {\"path\": \"relative path (REQUIRED)\"}",
    "compare_experiment_results": "Compare experiment results. Params: {\"path_a\": \"path (REQUIRED)\", \"path_b\": \"path (REQUIRED)\"}",
    "generate_experiment_report": "Generate experiment report. Params: {\"metrics_path\": \"path (REQUIRED)\"}",
    "generate_markdown_report": "Generate Markdown report. Params: {\"title\": \"title (REQUIRED)\", \"content\": \"content (REQUIRED)\"}",
    "generate_html_report": "Generate HTML report. Params: {\"title\": \"title (REQUIRED)\", \"content\": \"content (REQUIRED)\"}",
    "save_text_output": "Save text to file. Params: {\"content\": \"text (REQUIRED)\", \"filename\": \"optional filename\"}",
    "fetch_url": "Fetch URL content. Params: {\"url\": \"URL (REQUIRED)\"}",
    "search_web": "Web search. Params: {\"query\": \"search query (REQUIRED)\"}",
    "download_file": "Download file. Params: {\"url\": \"URL (REQUIRED)\", \"save_path\": \"workspace path (REQUIRED)\"}",
}


def get_tool_descriptions() -> str:
    lines = []
    for name, desc in TOOL_DESCRIPTIONS.items():
        lines.append(f"- {name}: {desc}")
    return "Available tools:\n" + "\n".join(lines)


def call_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    if tool_name not in TOOLS:
        return f"❌ 未知工具: {tool_name}"
    
    try:
        return TOOLS[tool_name](**arguments)
    except TypeError as e:
        # 捕获参数缺失，直接返回错误信息让 Agent 自我修正
        return f"⚠️ 参数错误: {str(e)}。请检查工具说明，确保 'arguments' 中包含所有必填参数。"
    except Exception as e:
        return f"❌ 工具执行失败: {str(e)}"
