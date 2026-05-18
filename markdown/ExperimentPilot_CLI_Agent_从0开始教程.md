# ExperimentPilot：從 0 開始寫一個 CLI Agent 教程

> 面向算法工程師 / 機器學習項目嘅 CLI Agent：可以喺終端理解任務、讀取文件、調用工具、執行安全命令、分析實驗結果、生成 Markdown 報告。呢份教程目標係幫你做一個可以寫入簡歷嘅 Agent 項目。

---

## 1. 項目定位

項目名建議：`ExperimentPilot`

一句話定位：

```text
ExperimentPilot is a CLI AI agent for machine learning experiment analysis, code understanding, and technical report generation.
```

你第一版 MVP 唔需要做成 Claude Code / Codex CLI 咁複雜，只需要做到：

1. 可以喺終端同 Agent 對話。
2. Agent 可以讀取文件、列出目錄、搜索文件、寫 Markdown。
3. Agent 可以根據任務自動選擇工具。
4. Agent 可以安全執行部分 shell 命令。
5. Agent 可以分析機器學習實驗結果並生成報告。

---

## 2. 技術棧選擇

推薦用 Python 開始，因為你係算法工程師，之後做 RAG、embedding、實驗分析、模型評估都方便。

| 模塊 | 推薦技術 |
|---|---|
| CLI 框架 | Typer |
| 終端美化 | Rich |
| LLM 調用 | OpenAI Python SDK / 兼容 OpenAI API 嘅模型服務 |
| 數據校驗 | Pydantic |
| 環境變量 | python-dotenv |
| 本地記憶 | JSON / SQLite |
| 測試 | pytest |
| 後續 RAG | Chroma / FAISS / sentence-transformers |

補充：OpenAI 官方 Python SDK 目前以 Responses API 作為主要接口之一；OpenAI Agents SDK 亦提供 tools、handoffs、tracing 等工程能力。你可以先自己實現輕量 Agent，理解底層邏輯之後，再考慮接入 Agents SDK 或 LangGraph。

參考資料：

- OpenAI Python SDK: https://github.com/openai/openai-python
- OpenAI Agents SDK: https://github.com/openai/openai-agents-python
- Agents SDK tracing: https://github.com/openai/openai-agents-python/blob/main/docs/tracing.md
- Agents SDK handoffs: https://github.com/openai/openai-agents-python/blob/main/docs/handoffs.md

---

## 3. 初始化項目

### 3.1 創建項目

```bash
mkdir experiment-pilot
cd experiment-pilot
```

### 3.2 創建虛擬環境

Windows：

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux：

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3.3 安裝依賴

```bash
pip install typer rich pydantic python-dotenv openai pytest
```

### 3.4 創建目錄結構

```bash
mkdir -p expilot/core expilot/tools expilot/memory expilot/utils tests examples .agent

touch expilot/__init__.py
touch expilot/main.py
touch expilot/core/agent.py
touch expilot/core/llm.py
touch expilot/core/schema.py
touch expilot/tools/file_tools.py
touch expilot/tools/shell_tools.py
touch expilot/tools/registry.py
touch expilot/memory/store.py
touch expilot/utils/config.py
```

最終結構：

```text
experiment-pilot/
├── expilot/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── agent.py
│   │   ├── llm.py
│   │   └── schema.py
│   ├── tools/
│   │   ├── file_tools.py
│   │   ├── shell_tools.py
│   │   └── registry.py
│   ├── memory/
│   │   └── store.py
│   └── utils/
│       └── config.py
├── tests/
├── examples/
├── .agent/
├── pyproject.toml
└── .env
```

---

## 4. 配置 pyproject.toml

喺根目錄新建 `pyproject.toml`：

```toml
[project]
name = "experiment-pilot"
version = "0.1.0"
description = "A CLI AI agent for ML experiment analysis, code understanding, and report generation."
requires-python = ">=3.10"
dependencies = [
    "typer",
    "rich",
    "pydantic",
    "python-dotenv",
    "openai",
]

[project.scripts]
expilot = "expilot.main:app"

[tool.pytest.ini_options]
pythonpath = ["."]
```

安裝成本地可編輯包：

```bash
pip install -e .
```

測試：

```bash
expilot --help
```

---

## 5. 配置環境變量

新建 `.env`：

```env
OPENAI_API_KEY=你的_API_KEY
EXPILOT_MODEL=gpt-4.1-mini
```

新建 `.gitignore`：

```gitignore
.venv/
.env
.agent/
__pycache__/
*.pyc
```

`.env` 唔好提交到 GitHub。

---

## 6. CLI 入口

編輯 `expilot/main.py`：

```python
import typer
from rich.console import Console
from expilot.core.agent import Agent

app = typer.Typer(help="ExperimentPilot: A CLI AI agent for ML experiments and code projects.")
console = Console()


@app.command()
def chat():
    """Start interactive chat mode."""
    agent = Agent()
    console.print("[bold green]ExperimentPilot Chat Mode[/bold green]")
    console.print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = console.input("[bold cyan]You:[/bold cyan] ")
        if user_input.strip().lower() in {"exit", "quit"}:
            console.print("[yellow]Bye![/yellow]")
            break

        answer = agent.run(user_input)
        console.print(f"[bold magenta]Agent:[/bold magenta] {answer}\n")


@app.command()
def run(task: str):
    """Run a single agent task."""
    agent = Agent()
    answer = agent.run(task)
    console.print(answer)
```

測試：

```bash
expilot chat
expilot run "你好，介紹一下你自己"
```

而家 `Agent` 未實現，下一步補。

---

## 7. 定義 Agent 行為 Schema

編輯 `expilot/core/schema.py`：

```python
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """A tool call requested by the agent."""
    tool_name: str = Field(..., description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(default_factory=dict)


class AgentAction(BaseModel):
    """Structured decision made by the LLM."""
    thought: str = Field(..., description="Short reasoning summary")
    action_type: str = Field(..., description="Either 'tool' or 'final'")
    tool_call: Optional[ToolCall] = None
    final_answer: Optional[str] = None
```

呢個 schema 用嚟約束模型輸出，令 Agent 可以穩定判斷：

```text
要調工具？
定係直接回答？
如果調工具，調邊個工具？
參數係咩？
```

---

## 8. 實現文件工具

編輯 `expilot/tools/file_tools.py`：

```python
from pathlib import Path
from typing import List


WORKSPACE = Path.cwd()


def _safe_path(path: str) -> Path:
    """Resolve path and prevent escaping workspace."""
    target = (WORKSPACE / path).resolve()
    workspace = WORKSPACE.resolve()

    if not str(target).startswith(str(workspace)):
        raise ValueError("Access outside workspace is not allowed")

    return target


def list_dir(path: str = ".") -> str:
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
    target = _safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"File written: {path}"


def search_files(keyword: str, path: str = ".", max_results: int = 20) -> str:
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
```

`_safe_path` 非常重要，可以防止 Agent 讀取工作區以外嘅敏感文件，例如 `../../.ssh/id_rsa`。

---

## 9. 實現 Shell 工具

編輯 `expilot/tools/shell_tools.py`：

```python
import subprocess
from typing import List
from rich.prompt import Confirm


DANGEROUS_KEYWORDS: List[str] = [
    "rm -rf",
    "del /s",
    "format",
    "shutdown",
    "reboot",
    ":(){",
    "mkfs",
]


def run_shell(command: str, timeout: int = 20, require_confirm: bool = True) -> str:
    """Run a shell command with simple safety checks."""
    lowered = command.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in lowered:
            return f"Blocked dangerous command: {command}"

    if require_confirm:
        if not Confirm.ask(f"About to run command: {command}. Continue?"):
            return "User cancelled command execution."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            return f"Command failed with code {result.returncode}\nSTDOUT:\n{output}\nSTDERR:\n{error}"

        return output or "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Command error: {e}"
```

---

## 10. 工具註冊表

編輯 `expilot/tools/registry.py`：

```python
from typing import Any, Callable, Dict
from expilot.tools.file_tools import list_dir, read_file, write_file, search_files
from expilot.tools.shell_tools import run_shell


TOOLS: Dict[str, Callable[..., str]] = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
    "run_shell": run_shell,
}


TOOL_DESCRIPTIONS = """
Available tools:

1. list_dir(path: str = ".")
   List files and directories under a path.

2. read_file(path: str, max_chars: int = 8000)
   Read a text file from workspace.

3. write_file(path: str, content: str)
   Write content to a file under workspace.

4. search_files(keyword: str, path: str = ".", max_results: int = 20)
   Search files by filename or text content.

5. run_shell(command: str, timeout: int = 20, require_confirm: bool = True)
   Run a shell command with safety checks.
"""


def call_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    if tool_name not in TOOLS:
        return f"Unknown tool: {tool_name}"

    tool = TOOLS[tool_name]
    try:
        return tool(**arguments)
    except Exception as e:
        return f"Tool execution error: {e}"
```

後續想加 `git_diff`、`analyze_csv`、`index_project`，只需要寫函數再註冊入 `TOOLS`。

---

## 11. LLM 調用層

編輯 `expilot/core/llm.py`：

```python
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from expilot.core.schema import AgentAction

load_dotenv()


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("EXPILOT_MODEL", "gpt-4.1-mini")

    def decide(self, system_prompt: str, user_prompt: str) -> AgentAction:
        """Ask the model to return a structured JSON action."""
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "agent_action",
                    "schema": AgentAction.model_json_schema(),
                    "strict": True,
                }
            },
        )

        raw = response.output_text
        data = json.loads(raw)
        return AgentAction.model_validate(data)
```

如果 SDK 版本唔支持 `text.format`，可以先用普通 JSON prompt：

```python
response = self.client.responses.create(
    model=self.model,
    input=system_prompt + "\n\n" + user_prompt,
)
raw = response.output_text
```

然後用 `json.loads(raw)` 解析。

---

## 12. Agent 主循環

編輯 `expilot/core/agent.py`：

```python
from rich.console import Console
from expilot.core.llm import LLMClient
from expilot.tools.registry import TOOL_DESCRIPTIONS, call_tool
from expilot.memory.store import MemoryStore


class Agent:
    def __init__(self, max_steps: int = 6):
        self.llm = LLMClient()
        self.max_steps = max_steps
        self.console = Console()
        self.memory = MemoryStore()

    def _system_prompt(self) -> str:
        return f"""
You are ExperimentPilot, a CLI AI agent for machine learning projects and code analysis.

You can solve tasks by either:
1. Calling a tool.
2. Giving a final answer.

You must return valid JSON that matches the required schema.

Rules:
- Use tools when you need to inspect files, list directories, write files, search files, or run commands.
- Do not guess file contents. Read files before analyzing them.
- Prefer small and safe steps.
- Do not run dangerous shell commands.
- If you have enough information, return final answer.
- Keep thought concise. Do not reveal hidden chain-of-thought.

{TOOL_DESCRIPTIONS}
"""

    def run(self, task: str) -> str:
        history = []

        for step in range(1, self.max_steps + 1):
            user_prompt = self._build_user_prompt(task, history)
            action = self.llm.decide(self._system_prompt(), user_prompt)

            if action.action_type == "final":
                return action.final_answer or "Task completed."

            if action.action_type == "tool" and action.tool_call:
                tool_name = action.tool_call.tool_name
                arguments = action.tool_call.arguments

                self.console.print(f"[dim]Step {step}: calling tool {tool_name} with {arguments}[/dim]")
                observation = call_tool(tool_name, arguments)

                history.append({
                    "thought": action.thought,
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "observation": observation,
                })
                continue

            return "Agent produced an invalid action."

        return "Reached max steps. Please narrow the task or increase max_steps."

    def _build_user_prompt(self, task: str, history: list) -> str:
        memories = self.memory.list()
        return f"""
User task:
{task}

Known user/project memories:
{memories}

Previous steps and observations:
{history}

Decide the next action.
"""
```

呢個就係核心循環：

```text
用戶任務 → 模型決策 → 工具調用 → 觀察結果 → 再決策 → 最終回答
```

---

## 13. 本地 Memory

編輯 `expilot/memory/store.py`：

```python
import json
from pathlib import Path
from typing import Any, Dict, List


class MemoryStore:
    def __init__(self, path: str = ".agent/memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text(
                json.dumps({"memories": []}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def load(self) -> Dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add(self, item: str) -> None:
        data = self.load()
        data.setdefault("memories", []).append(item)
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list(self) -> List[str]:
        return self.load().get("memories", [])
```

第一版 memory 可以保存：項目名、常用路徑、用戶偏好、歷史任務摘要。後續可以加自動總結保存。

---

## 14. 測試最小可用 Agent

運行：

```bash
expilot run "列出當前目錄有哪些文件"
```

理想情況：

```text
Step 1: calling tool list_dir with {'path': '.'}
Agent: 当前目录包含...
```

再試：

```bash
expilot run "讀取 pyproject.toml，總結呢個項目係做咩嘅"
```

再試生成文件：

```bash
expilot run "幫我創建 examples/demo.md，內容係呢個項目嘅簡介"
```

檢查：

```bash
cat examples/demo.md
```

---

## 15. 加入機器學習實驗分析能力

創建 `expilot/tools/ml_tools.py`：

```python
import json
from pathlib import Path
from typing import Any, Dict


def summarize_json_metrics(path: str) -> str:
    file = Path(path)
    if not file.exists():
        return f"Metrics file not found: {path}"

    data: Dict[str, Any] = json.loads(file.read_text(encoding="utf-8"))

    lines = ["Experiment Metrics Summary:"]
    for key, value in data.items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)
```

喺 `registry.py` 加：

```python
from expilot.tools.ml_tools import summarize_json_metrics
TOOLS["summarize_json_metrics"] = summarize_json_metrics
```

`TOOL_DESCRIPTIONS` 加：

```text
6. summarize_json_metrics(path: str)
   Read a JSON metrics file and summarize experiment metrics.
```

創建測試 metrics：

```bash
mkdir -p experiments
cat > experiments/metrics.json <<'JSON_BLOCK'
{
  "accuracy": 0.932,
  "precision": 0.918,
  "recall": 0.901,
  "f1": 0.909,
  "loss": 0.183
}
JSON_BLOCK
```

測試：

```bash
expilot run "讀取 experiments/metrics.json，幫我寫一段實驗結果分析"
```

---

## 16. 報告生成能力

可以直接用 `write_file` 生成 Markdown 報告。

示例：

```bash
expilot run "讀取 experiments/metrics.json，生成 reports/experiment_report.md，包括實驗結果、問題分析、改進方向"
```

理想流程：

```text
1. read_file experiments/metrics.json
2. 分析指標
3. write_file reports/experiment_report.md
4. final answer
```

報告模板：

```markdown
# 實驗報告

## 1. 實驗目的
## 2. 數據與方法
## 3. 指標結果
## 4. 結果分析
## 5. 異常問題與解決方案
## 6. 後續改進方向
```

---

## 17. 加入測試

創建 `tests/test_file_tools.py`：

```python
from expilot.tools.file_tools import list_dir, write_file, read_file


def test_write_and_read_file():
    result = write_file(".agent/test.txt", "hello")
    assert "File written" in result

    content = read_file(".agent/test.txt")
    assert content == "hello"


def test_list_dir():
    result = list_dir(".")
    assert isinstance(result, str)
```

運行：

```bash
pytest
```

---

## 18. README 寫法

建議 README 結構：

```markdown
# ExperimentPilot

A CLI AI agent for machine learning experiment analysis, code understanding, and report generation.

## Features

- Interactive CLI chat mode
- Plan-Act-Observe agent loop
- Tool calling
- File read/write/list/search tools
- Safe shell execution
- Local memory
- ML experiment metrics analysis
- Markdown report generation

## Architecture

User Task → Planner → Tool Selection → Tool Execution → Observation → Final Answer

## Quick Start

...

## Demo

...

## Roadmap

- RAG-based project indexing
- Git diff analysis
- Test generation
- Code review mode
- Docker sandbox
- Multi-agent workflow
```

README 最好放終端截圖或者 GIF，對 GitHub 展示好重要。

---

## 19. 後續升級：RAG 項目理解

可以加：

```bash
expilot index .
expilot ask "訓練流程喺邊個文件入面？"
```

RAG 流程：

```text
掃描項目文件
→ 切分 chunk
→ embedding 編碼
→ 存入向量庫
→ 查詢時召回相關 chunk
→ 放入 Agent 上下文
→ 回答問題
```

推薦模塊：

```text
expilot/rag/indexer.py
expilot/rag/retriever.py
expilot/rag/chunker.py
```

---

## 20. 後續升級：Git diff 分析

新增工具：

```text
git_status
git_diff
git_log
```

示例：

```bash
expilot run "分析今次 git diff 有冇潛在 bug"
```

理想流程：

```text
run_shell git diff
→ 分析修改內容
→ 指出風險
→ 提出修復建議
```

---

## 21. 後續升級：代碼修復模式

可以設計：

```bash
expilot fix "根據 logs/error.txt 修復 bug"
```

流程：

```text
讀取錯誤日誌
→ 搜索相關代碼
→ 分析原因
→ 生成 patch
→ 用戶確認
→ 寫入文件
```

改文件前一定要確認，避免 Agent 亂改代碼。

---

## 22. 後續升級：多 Agent 架構

可以拆成：

```text
PlannerAgent：拆解任務
CoderAgent：分析同修改代碼
ResearchAgent：檢索資料
ReportAgent：生成報告
CriticAgent：檢查輸出質量
```

做到呢一步，可以考慮用 OpenAI Agents SDK 或 LangGraph 管理 workflow。

---

## 23. 常見問題

### 問題 1：模型輸出唔係合法 JSON

解法：

1. 使用 structured outputs。
2. prompt 入面強制要求 JSON。
3. 加 JSON parse 失敗重試。
4. 降低 temperature。

### 問題 2：Agent 一直調工具唔停

解法：

1. 設置 `max_steps`。
2. prompt 入面寫明信息足夠就 final。
3. 記錄歷史工具調用，避免重複。

### 問題 3：文件太長，上下文爆炸

解法：

1. `read_file` 加 `max_chars`。
2. 先搜索再讀取。
3. 引入 RAG。
4. 對長文件做摘要緩存。

### 問題 4：Shell 命令危險

解法：

1. 危險命令黑名單。
2. 人工確認。
3. Docker sandbox。
4. 命令白名單。

### 問題 5：項目太似普通 API demo

解法：

1. 展示工具調用流程。
2. 加 ML 實驗分析 demo。
3. 加 RAG。
4. 加測試。
5. 加架構圖。
6. 加安全機制。

---

## 24. 推薦開發順序

```text
Day 1：CLI 入口 + LLM 對話
Day 2：文件工具 + 工具註冊表
Day 3：Agent 主循環
Day 4：Shell 工具 + 安全確認
Day 5：Memory + 日誌
Day 6：實驗指標分析工具
Day 7：README + Demo + 測試 + 簡歷描述
後續：RAG、Git diff、代碼修復、多 Agent
```

---

## 25. MVP 驗收標準

做到以下幾點，就算第一版完成：

1. `expilot chat` 可以正常交互。
2. `expilot run "列出當前目錄"` 可以調 `list_dir`。
3. `expilot run "讀取 README.md 並總結"` 可以調 `read_file`。
4. `expilot run "生成 reports/demo.md"` 可以調 `write_file`。
5. Shell 命令有安全攔截或確認。
6. 有 memory 文件。
7. 有 ML metrics 分析 demo。
8. 有 README。
9. 有測試。
10. 可以放上 GitHub 展示。

---

## 26. 簡歷寫法

中文：

```text
- 獨立設計並實現一個面向機器學習實驗分析的 CLI Agent，支持終端交互、工具調用、文件讀寫、Shell 執行和 Markdown 報告生成。
- 實現 Plan-Act-Observe Agent 主循環，使模型能夠根據任務自動選擇工具並進行多步執行。
- 設計插件式工具註冊機制，支持文件系統工具、實驗指標分析工具和安全命令執行工具擴展。
- 引入本地 Memory 和執行歷史，用於保存項目上下文並提升多輪任務連續性。
- 增加危險命令攔截與人工確認機制，提高 Agent 在真實開發環境中的安全性。
```

英文：

```text
- Built ExperimentPilot, a CLI-based AI agent for machine learning experiment analysis, code understanding, and report generation.
- Implemented a Plan-Act-Observe loop with structured tool calling for multi-step task execution.
- Designed a plugin-style tool registry supporting file operations, shell execution, and experiment metrics analysis.
- Added local memory and execution history to improve contextual continuity across tasks.
- Implemented safety checks and human-in-the-loop confirmation for risky command execution.
```

---

## 27. 總結

呢個項目最有價值嘅地方唔係“調一次 API”，而係你展示咗完整 Agent 工程能力：

```text
CLI 交互
工具調用
任務規劃
文件操作
安全機制
本地記憶
實驗分析
報告生成
工程測試
項目文檔
```

對算法工程師嚟講，最推薦定位係：

```text
面向機器學習實驗同代碼項目分析嘅 CLI Agent
```

咁樣既貼合你嘅背景，又比普通聊天機器人更有技術含量。後續你再加 RAG、Git diff 分析、代碼修復、多 Agent 協作，就可以變成一個真正能夠寫入簡歷、面試時可以深入講解嘅項目。
