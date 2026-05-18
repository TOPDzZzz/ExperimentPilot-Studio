# 從 0 開始構建「通用多功能可視化 Agent」詳細指導書

> 項目定位：由原本 CLI Agent 升級成一個有 Web 可視化界面、工具調用、多任務能力、記憶系統、RAG 知識庫、文件處理、代碼助手、研究助手、數據分析助手和任務規劃能力的通用 Agent 平台。

---

## 1. 項目總目標

你要做的不是一個普通聊天機器人，而是一個可以真正「執行任務」的 Agent 系統。

普通聊天機器人流程：

```text
User -> LLM -> Answer
```

Agent 系統流程：

```text
User -> 任務理解 -> 任務規劃 -> 工具選擇 -> 工具執行 -> 觀察結果 -> 反思修正 -> 最終輸出
```

所以這個項目要突出以下能力：

1. 有可視化界面，不只是命令行。
2. 可以調用工具，例如讀文件、寫文件、執行命令、分析代碼、解析文檔、分析表格。
3. 可以處理多類任務，不局限於機器學習。
4. 有記憶系統，可以保存用戶偏好、歷史任務和項目上下文。
5. 有本地知識庫 / RAG，可以基於文檔回答問題。
6. 有工具調用 Trace，可視化展示 Agent 每一步做了什麼。
7. 有安全控制，高風險操作需要確認或直接攔截。

推薦項目名：

```text
AgentHub Studio
```

定位：

```text
A visual multi-purpose AI agent platform with tool-calling, RAG, memory, file processing, code analysis and task planning.
```

---

## 2. 最終效果

完成後，你可以啟動本地 Web 界面：

```bash
streamlit run app.py
```

瀏覽器打開：

```text
http://localhost:8501
```

界面包含：

```text
1. Chat Agent：通用對話助手
2. File Assistant：文件助手
3. Code Assistant：代碼助手
4. Data Assistant：數據分析助手
5. Research Assistant：研究助手
6. Knowledge Base：本地知識庫 / RAG
7. Task Planner：任務規劃器
8. Tool Trace：工具調用日誌
9. Settings：模型、路徑和安全設置
```

---

## 3. 技術選型

### 3.1 第一版推薦：Streamlit + Python

適合快速做出可展示版本。

```text
前端界面：Streamlit
後端語言：Python
LLM 接入：OpenAI SDK / LiteLLM
Agent 編排：自寫 Agent Loop
本地存儲：JSON + SQLite
文檔解析：pypdf / python-docx / pandas
向量庫：Chroma
配置管理：python-dotenv / pydantic
終端與日誌：rich / logging
```

優點：

```text
1. 開發快
2. Python 對算法工程師友好
3. 一個人 2-3 星期可以做出完整 demo
4. 適合先完成簡歷項目
```

### 3.2 第二版進階：FastAPI + React

等第一版完成後，可以重構成更工程化版本：

```text
前端：React + Vite + TailwindCSS
後端：FastAPI
通信：REST API + WebSocket
數據庫：SQLite / PostgreSQL
向量庫：Chroma / Qdrant
Agent 框架：LangGraph / OpenAI Agents SDK
部署：Docker
```

FastAPI 適合做高性能 API 服務，官方文檔亦提供 WebSocket 支持；Streamlit 則適合快速構建聊天和多頁面數據應用。OpenAI Agents SDK 支持工具、handoff、tracing、MCP 等 Agent 工程能力；LangGraph 適合長流程、有狀態、多步驟 Agent 工作流。

---

## 4. 項目目錄結構

建議使用以下結構：

```text
agenthub-studio/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── agenthub/
│   ├── core/
│   │   ├── agent.py
│   │   ├── llm_agent.py
│   │   ├── planner.py
│   │   ├── tool_router.py
│   │   ├── memory.py
│   │   ├── trace.py
│   │   ├── profiles.py
│   │   └── config.py
│   │
│   ├── tools/
│   │   ├── file_tools.py
│   │   ├── shell_tools.py
│   │   ├── code_tools.py
│   │   ├── data_tools.py
│   │   ├── report_tools.py
│   │   └── web_tools.py
│   │
│   ├── rag/
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── ui/
│   │   ├── components/
│   │   │   ├── sidebar.py
│   │   │   ├── trace_viewer.py
│   │   │   └── file_uploader.py
│   │   └── pages/
│   │       ├── chat_page.py
│   │       ├── file_page.py
│   │       ├── code_page.py
│   │       ├── data_page.py
│   │       ├── rag_page.py
│   │       └── settings_page.py
│   │
│   └── storage/
│       ├── memory.json
│       ├── traces.json
│       └── tasks.db
│
├── pages/
│   ├── 1_💬_Chat_Agent.py
│   ├── 2_📁_File_Assistant.py
│   ├── 3_💻_Code_Assistant.py
│   ├── 4_📊_Data_Assistant.py
│   ├── 5_📚_Knowledge_Base.py
│   ├── 6_🧭_Tool_Trace.py
│   └── 7_⚙️_Settings.py
│
├── workspace/
├── uploads/
├── outputs/
└── tests/
```

---

## 5. 開發環境搭建

### 5.1 創建 D 盤 Conda 環境

```bash
conda create -p D:\conda_envs\agenthub python=3.11
```

啟動：

```bash
conda activate D:\conda_envs\agenthub
```

### 5.2 創建項目

```bash
D:
mkdir projects
cd projects
mkdir agenthub-studio
cd agenthub-studio
```

### 5.3 requirements.txt

```txt
openai
python-dotenv
streamlit
typer
rich
pydantic
pandas
openpyxl
pypdf
python-docx
chromadb
tiktoken
numpy
scikit-learn
fastapi
uvicorn
```

安裝：

```bash
pip install -r requirements.txt
```

### 5.4 .env

```env
OPENAI_API_KEY=你的_api_key
MODEL_NAME=gpt-4.1-mini
```

### 5.5 .gitignore

```gitignore
.env
__pycache__/
*.pyc
uploads/
outputs/
agenthub/storage/*.db
agenthub/storage/*.json
agenthub/storage/chroma/
```

---

## 6. 第一版：可視化 Chat Agent

創建 `app.py`：

```python
import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AgentHub Studio",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AgentHub Studio")
st.caption("一個通用多功能可視化 Agent 平台")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("輸入你的任務，例如：幫我分析文件 / 解釋代碼 / 生成計劃")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent 正在思考..."):
            response = client.responses.create(
                model=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
                input=user_input
            )
            answer = response.output_text
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
```

運行：

```bash
streamlit run app.py
```

---

## 7. 第二版：加入工具系統

工具是 Agent 的手腳。LLM 負責理解和決策，工具負責執行真實操作。

### 7.1 文件工具

創建 `agenthub/tools/file_tools.py`：

```python
from pathlib import Path

WORKSPACE = Path("workspace")
WORKSPACE.mkdir(exist_ok=True)

def safe_path(path: str) -> Path:
    full_path = (WORKSPACE / path).resolve()
    workspace_root = WORKSPACE.resolve()

    if not str(full_path).startswith(str(workspace_root)):
        raise ValueError("非法路徑：不能訪問 workspace 之外的文件")

    return full_path

def list_dir(path: str = ".") -> str:
    target = safe_path(path)

    if not target.exists():
        return f"路徑不存在：{path}"

    if not target.is_dir():
        return f"不是文件夾：{path}"

    items = []
    for item in target.iterdir():
        prefix = "[DIR]" if item.is_dir() else "[FILE]"
        items.append(f"{prefix} {item.name}")

    return "\n".join(items)

def read_file(path: str) -> str:
    target = safe_path(path)

    if not target.exists():
        return f"文件不存在：{path}"

    if not target.is_file():
        return f"不是文件：{path}"

    return target.read_text(encoding="utf-8", errors="ignore")

def write_file(path: str, content: str) -> str:
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"文件已寫入：{path}"
```

### 7.2 工具路由

創建 `agenthub/core/tool_router.py`：

```python
from agenthub.tools.file_tools import list_dir, read_file, write_file

TOOLS = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
}

def call_tool(tool_name: str, arguments: dict) -> str:
    if tool_name not in TOOLS:
        return f"未知工具：{tool_name}"

    try:
        result = TOOLS[tool_name](**arguments)
        return result
    except Exception as e:
        return f"工具執行失敗：{str(e)}"
```

---

## 8. 第三版：LLM 自動選擇工具

### 8.1 Prompt

創建 `agenthub/core/prompts.py`：

```python
TOOL_DECISION_PROMPT = """
你是一個可調用工具的 Agent。

你可以使用以下工具：

1. list_dir
   描述：列出 workspace 中的文件和文件夾
   參數：{"path": "相對路徑"}

2. read_file
   描述：讀取 workspace 中的文件
   參數：{"path": "相對路徑"}

3. write_file
   描述：寫入文件到 workspace
   參數：{"path": "相對路徑", "content": "文件內容"}

請根據用戶任務，輸出 JSON。

如果需要調工具：
{
  "type": "tool",
  "tool_name": "工具名",
  "arguments": {}
}

如果不需要調工具：
{
  "type": "answer",
  "content": "直接回答內容"
}

只能輸出 JSON，不要輸出其他文字。
"""
```

### 8.2 LLM Agent

創建 `agenthub/core/llm_agent.py`：

```python
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from agenthub.core.prompts import TOOL_DECISION_PROMPT
from agenthub.core.tool_router import call_tool

load_dotenv()

class LLMAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("MODEL_NAME", "gpt-4.1-mini")

    def decide(self, user_input: str) -> dict:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": TOOL_DECISION_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )

        text = response.output_text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"type": "answer", "content": text}

    def run(self, user_input: str) -> str:
        decision = self.decide(user_input)

        if decision.get("type") == "tool":
            tool_name = decision.get("tool_name")
            arguments = decision.get("arguments", {})
            tool_result = call_tool(tool_name, arguments)

            final_response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": "你是一個助手，請根據工具返回結果，用清晰方式回答用戶。"},
                    {"role": "user", "content": f"用戶任務：{user_input}\n工具結果：{tool_result}"}
                ]
            )

            return final_response.output_text

        return decision.get("content", "沒有生成有效回答")
```

---

## 9. 第四版：加入 Trace 工具調用日誌

### 9.1 trace.py

創建 `agenthub/core/trace.py`：

```python
import time
import json
from pathlib import Path

TRACE_PATH = Path("agenthub/storage/traces.json")
TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_trace(step_type: str, name: str, input_data: dict, output_data: str):
    trace = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "step_type": step_type,
        "name": name,
        "input": input_data,
        "output_preview": output_data[:500]
    }

    if TRACE_PATH.exists():
        traces = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
    else:
        traces = []

    traces.append(trace)
    TRACE_PATH.write_text(json.dumps(traces, ensure_ascii=False, indent=2), encoding="utf-8")

def load_traces():
    if not TRACE_PATH.exists():
        return []
    return json.loads(TRACE_PATH.read_text(encoding="utf-8"))
```

### 9.2 修改 tool_router.py

```python
from agenthub.tools.file_tools import list_dir, read_file, write_file
from agenthub.core.trace import log_trace

TOOLS = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
}

def call_tool(tool_name: str, arguments: dict) -> str:
    if tool_name not in TOOLS:
        return f"未知工具：{tool_name}"

    try:
        result = TOOLS[tool_name](**arguments)
        log_trace("tool", tool_name, arguments, result)
        return result
    except Exception as e:
        error = f"工具執行失敗：{str(e)}"
        log_trace("tool_error", tool_name, arguments, error)
        return error
```

### 9.3 在 UI 顯示 Trace

在 `app.py` 或 Trace 頁面加入：

```python
import streamlit as st
from agenthub.core.trace import load_traces

st.title("🧭 Tool Trace")

traces = load_traces()

for trace in traces[::-1]:
    with st.expander(f"{trace['step_type']} - {trace['name']} - {trace['timestamp']}"):
        st.write("輸入：")
        st.json(trace["input"])
        st.write("輸出摘要：")
        st.text(trace["output_preview"])
```

---

## 10. 第五版：多頁面 UI

創建 `pages` 目錄：

```text
pages/
├── 1_💬_Chat_Agent.py
├── 2_📁_File_Assistant.py
├── 3_💻_Code_Assistant.py
├── 4_📊_Data_Assistant.py
├── 5_📚_Knowledge_Base.py
├── 6_🧭_Tool_Trace.py
└── 7_⚙️_Settings.py
```

Streamlit 會自動識別 `pages` 目錄，側邊欄會出現頁面導航。

---

## 11. File Assistant：文件助手

創建 `pages/2_📁_File_Assistant.py`：

```python
import streamlit as st
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

st.title("📁 File Assistant")

uploaded_file = st.file_uploader(
    "上傳文件",
    type=["txt", "md", "pdf", "docx", "csv", "xlsx"]
)

if uploaded_file:
    save_path = UPLOAD_DIR / uploaded_file.name
    save_path.write_bytes(uploaded_file.getbuffer())
    st.success(f"文件已上傳：{save_path}")

    if uploaded_file.name.endswith((".txt", ".md")):
        text = save_path.read_text(encoding="utf-8", errors="ignore")
        st.text_area("文件內容", text, height=400)
    else:
        st.info("PDF / DOCX / Excel 解析會在 loader.py 中實現")
```

---

## 12. 文件解析模塊

創建 `agenthub/rag/loader.py`：

```python
from pathlib import Path
from pypdf import PdfReader
import docx
import pandas as pd

def load_txt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)

def load_docx(path: str) -> str:
    document = docx.Document(path)
    return "\n".join([p.text for p in document.paragraphs])

def load_csv(path: str) -> str:
    df = pd.read_csv(path)
    return df.to_markdown(index=False)

def load_excel(path: str) -> str:
    df = pd.read_excel(path)
    return df.to_markdown(index=False)

def load_document(path: str) -> str:
    suffix = Path(path).suffix.lower()

    if suffix in [".txt", ".md"]:
        return load_txt(path)
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix == ".docx":
        return load_docx(path)
    if suffix == ".csv":
        return load_csv(path)
    if suffix in [".xls", ".xlsx"]:
        return load_excel(path)

    raise ValueError(f"不支持的文件類型：{suffix}")
```

---

## 13. RAG 知識庫

### 13.1 文本切分

創建 `agenthub/rag/splitter.py`：

```python
def split_text(text: str, chunk_size: int = 800, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks
```

### 13.2 Chroma 向量庫

創建 `agenthub/rag/vector_store.py`：

```python
import chromadb

class ChromaStore:
    def __init__(self, persist_dir: str = "agenthub/storage/chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="agenthub_knowledge"
        )

    def add_documents(self, chunks: list[str], source: str):
        ids = [f"{source}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source, "chunk_id": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, query: str, top_k: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        return results
```

### 13.3 檢索器

創建 `agenthub/rag/retriever.py`：

```python
from agenthub.rag.vector_store import ChromaStore

class Retriever:
    def __init__(self):
        self.store = ChromaStore()

    def retrieve(self, query: str, top_k: int = 5) -> str:
        results = self.store.search(query, top_k=top_k)
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        context_parts = []
        for doc, meta in zip(documents, metadatas):
            context_parts.append(f"來源：{meta.get('source')}\n內容：{doc}")

        return "\n\n---\n\n".join(context_parts)
```

---

## 14. Knowledge Base 頁面

創建 `pages/5_📚_Knowledge_Base.py`：

```python
import streamlit as st
from pathlib import Path
from agenthub.rag.loader import load_document
from agenthub.rag.splitter import split_text
from agenthub.rag.vector_store import ChromaStore
from agenthub.rag.retriever import Retriever

st.title("📚 Knowledge Base")

uploaded_file = st.file_uploader(
    "上傳文檔加入知識庫",
    type=["txt", "md", "pdf", "docx", "csv", "xlsx"]
)

if uploaded_file:
    path = Path("uploads") / uploaded_file.name
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(uploaded_file.getbuffer())

    if st.button("加入知識庫"):
        text = load_document(str(path))
        chunks = split_text(text)
        store = ChromaStore()
        store.add_documents(chunks, source=uploaded_file.name)
        st.success(f"已加入知識庫，共 {len(chunks)} 個 chunks")

query = st.text_input("向知識庫提問")

if st.button("檢索") and query:
    retriever = Retriever()
    context = retriever.retrieve(query)
    st.text_area("檢索結果", context, height=400)
```

---

## 15. 多 Agent 模式

創建 `agenthub/core/profiles.py`：

```python
AGENT_PROFILES = {
    "general": {
        "name": "General Agent",
        "system_prompt": "你是一個通用助手，擅長任務拆解、解釋和執行。"
    },
    "file": {
        "name": "File Assistant",
        "system_prompt": "你是一個文件處理助手，擅長總結、改寫、提取重點和生成報告。"
    },
    "code": {
        "name": "Code Assistant",
        "system_prompt": "你是一個代碼助手，擅長閱讀項目、解釋代碼、定位錯誤和生成測試。"
    },
    "research": {
        "name": "Research Assistant",
        "system_prompt": "你是一個研究助手，擅長整理資料、對比方案和生成研究報告。"
    },
    "data": {
        "name": "Data Analyst",
        "system_prompt": "你是一個數據分析助手，擅長分析 CSV、Excel 和生成可視化建議。"
    }
}
```

在 UI 中選擇模式：

```python
import streamlit as st
from agenthub.core.profiles import AGENT_PROFILES

mode = st.sidebar.selectbox(
    "選擇 Agent 模式",
    options=list(AGENT_PROFILES.keys()),
    format_func=lambda x: AGENT_PROFILES[x]["name"]
)
```

---

## 16. Code Assistant

創建 `agenthub/tools/code_tools.py`：

```python
from pathlib import Path

CODE_SUFFIXES = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs"]

def scan_code_project(root: str = "workspace") -> str:
    root_path = Path(root)

    if not root_path.exists():
        return f"路徑不存在：{root}"

    files = []
    for path in root_path.rglob("*"):
        if path.is_file() and path.suffix in CODE_SUFFIXES:
            files.append(str(path))

    return "\n".join(files)

def read_code_file(path: str) -> str:
    file_path = Path(path)

    if not file_path.exists():
        return f"文件不存在：{path}"

    return file_path.read_text(encoding="utf-8", errors="ignore")
```

代碼分析 Prompt：

```python
CODE_ANALYSIS_PROMPT = """
你是一個資深軟件工程師。
請根據以下代碼內容分析：

1. 文件功能
2. 核心類與函數
3. 主要執行流程
4. 潛在問題
5. 可優化建議
6. 是否需要補充測試

請用清晰 Markdown 輸出。
"""
```

---

## 17. Data Assistant

創建 `agenthub/tools/data_tools.py`：

```python
import pandas as pd

def analyze_csv(path: str) -> str:
    df = pd.read_csv(path)

    info = []
    info.append(f"行數：{df.shape[0]}")
    info.append(f"列數：{df.shape[1]}")
    info.append(f"列名：{list(df.columns)}")
    info.append("\n缺失值統計：")
    info.append(str(df.isnull().sum()))
    info.append("\n數值統計：")
    info.append(str(df.describe()))

    return "\n".join(info)

def analyze_excel(path: str) -> str:
    df = pd.read_excel(path)

    info = []
    info.append(f"行數：{df.shape[0]}")
    info.append(f"列數：{df.shape[1]}")
    info.append(f"列名：{list(df.columns)}")
    info.append("\n缺失值統計：")
    info.append(str(df.isnull().sum()))
    info.append("\n數值統計：")
    info.append(str(df.describe()))

    return "\n".join(info)
```

可以展示 demo：

```text
上傳 CSV -> Agent 自動分析字段、缺失值、數值統計 -> 生成分析報告
```

---

## 18. Shell 工具與安全控制

創建 `agenthub/tools/shell_tools.py`：

```python
import subprocess

DANGEROUS_KEYWORDS = [
    "rm -rf",
    "del /s",
    "format",
    "shutdown",
    "reboot",
    "diskpart",
    "reg delete"
]

def is_dangerous(command: str) -> bool:
    lower_cmd = command.lower()
    return any(keyword in lower_cmd for keyword in DANGEROUS_KEYWORDS)

def run_shell(command: str, allow_dangerous: bool = False) -> str:
    if is_dangerous(command) and not allow_dangerous:
        return f"高風險命令已被攔截：{command}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20
        )

        return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return "命令執行超時"
    except Exception as e:
        return f"命令執行失敗：{str(e)}"
```

安全原則：

```text
1. 默認只能訪問 workspace 目錄。
2. 高風險 Shell 命令直接攔截。
3. 寫文件前可顯示預覽。
4. 刪除文件、覆蓋文件、執行命令需要確認。
5. 不讓 Agent 直接操作系統核心目錄。
```

---

## 19. Memory 記憶系統

創建 `agenthub/core/memory.py`：

```python
import json
from pathlib import Path

MEMORY_PATH = Path("agenthub/storage/memory.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_memory() -> dict:
    if not MEMORY_PATH.exists():
        return {
            "user_preferences": {},
            "recent_tasks": [],
            "project_context": {}
        }

    return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))

def save_memory(memory: dict):
    MEMORY_PATH.write_text(
        json.dumps(memory, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def add_recent_task(task: str):
    memory = load_memory()
    memory.setdefault("recent_tasks", [])
    memory["recent_tasks"].append(task)
    memory["recent_tasks"] = memory["recent_tasks"][-20:]
    save_memory(memory)
```

可以記錄：

```text
1. 常用語言
2. 常用項目路徑
3. 最近任務
4. 生成過的報告
5. 用戶偏好的輸出格式
```

---

## 20. UI 設計建議

### 20.1 首頁 Dashboard

可以顯示：

```text
今日任務數
工具調用次數
知識庫文檔數
生成報告數
最近錯誤數
```

示例：

```python
col1, col2, col3, col4 = st.columns(4)

col1.metric("今日任務", "12")
col2.metric("工具調用", "48")
col3.metric("知識庫文檔", "7")
col4.metric("生成報告", "5")
```

### 20.2 Chat 頁面布局

```text
左側：Agent 模式、模型選擇、工具開關
中間：聊天窗口
右側：工具 Trace、任務步驟
```

### 20.3 File 頁面布局

```text
上方：文件上傳
左側：文件列表
中間：文件預覽
右側：總結、提取、生成報告按鈕
```

### 20.4 Knowledge Base 頁面布局

```text
左側：已入庫文件
中間：提問框
下方：檢索片段
右側：引用來源
```

---

## 21. 14 天開發計劃

### Day 1：項目初始化

任務：

```text
1. 創建 conda 環境
2. 創建項目結構
3. 安裝依賴
4. 寫第一個 Streamlit 頁面
```

交付物：

```text
可以打開 Web Chat 頁面
```

### Day 2：接入 LLM

任務：

```text
1. 配置 .env
2. 接入 OpenAI SDK
3. 完成普通對話
4. 保存 session_state 對話記錄
```

交付物：

```text
可以和 Agent 多輪聊天
```

### Day 3：文件工具

任務：

```text
1. read_file
2. write_file
3. list_dir
4. 路徑安全檢查
```

交付物：

```text
Agent 可以讀寫 workspace 文件
```

### Day 4：工具路由

任務：

```text
1. tool_router
2. 工具註冊表
3. call_tool
4. 初步工具調用日誌
```

交付物：

```text
統一工具調用入口
```

### Day 5：LLM 工具決策

任務：

```text
1. 設計工具選擇 prompt
2. 要求 LLM 輸出 JSON
3. 解析 JSON
4. 執行工具
5. 根據工具結果回答
```

交付物：

```text
Agent 可以自動決定是否調工具
```

### Day 6：Trace Viewer

任務：

```text
1. 記錄工具調用
2. 記錄輸入輸出
3. 在側邊欄展示 trace
4. 加錯誤記錄
```

交付物：

```text
可視化工具調用流程
```

### Day 7：多頁面 UI

任務：

```text
1. Chat 頁
2. File 頁
3. Trace 頁
4. Settings 頁
```

交付物：

```text
有完整可視化框架
```

### Day 8：文件解析

任務：

```text
1. txt / md
2. pdf
3. docx
4. csv / xlsx
```

交付物：

```text
可以上傳並解析多種文件
```

### Day 9：文件總結與報告生成

任務：

```text
1. 文件摘要 prompt
2. 重點提取
3. Markdown 報告生成
4. 輸出到 outputs
```

交付物：

```text
File Assistant 可用
```

### Day 10：RAG 知識庫

任務：

```text
1. 文本切分
2. Chroma 向量庫
3. 文檔入庫
4. 問答檢索
```

交付物：

```text
Knowledge Base 可用
```

### Day 11：Code Assistant

任務：

```text
1. 掃描代碼項目
2. 讀取代碼文件
3. 代碼分析 prompt
4. 生成項目結構報告
```

交付物：

```text
Code Assistant 可用
```

### Day 12：Data Assistant

任務：

```text
1. CSV 分析
2. Excel 分析
3. 缺失值統計
4. 數值統計
5. 生成分析建議
```

交付物：

```text
Data Assistant 可用
```

### Day 13：安全控制與記憶

任務：

```text
1. Shell 命令安全攔截
2. workspace 限制
3. memory.json
4. 用戶偏好保存
```

交付物：

```text
Agent 更安全，有基本記憶
```

### Day 14：README + Demo + 簡歷整理

任務：

```text
1. 補 README
2. 截圖
3. 錄製 demo gif
4. 寫簡歷描述
5. 整理 GitHub
```

交付物：

```text
可以放簡歷和 GitHub 的完整項目
```

---

## 22. README 寫法

建議 README 結構：

```markdown
# AgentHub Studio

A visual multi-purpose AI agent platform with tool-calling, RAG, memory, file processing, code analysis and task planning.

## Features

- Visual chat interface
- Tool-calling agent loop
- File assistant
- Code assistant
- Data assistant
- Research assistant
- Local RAG knowledge base
- Task planner
- Tool trace viewer
- Human-in-the-loop safety control

## Architecture

放架構圖

## Quick Start

安裝、配置、運行

## Demo

放截圖 / GIF

## Roadmap

列後續功能
```

---

## 23. 簡歷寫法

英文版：

```text
AgentHub Studio: Built a visual multi-purpose AI agent platform with Streamlit, Python and LLM APIs, supporting tool-calling, file processing, code analysis, local RAG knowledge base, task planning, memory management and execution tracing.
```

更詳細版本：

```text
- Designed and implemented a visual AI agent platform with multi-mode assistants for file analysis, code understanding, research summarization and data analysis.
- Built a tool-calling execution loop with file tools, shell tools, code tools and data analysis tools.
- Implemented a local RAG pipeline using document parsing, chunking, vector retrieval and LLM-grounded response generation.
- Added execution tracing, task logging and human-in-the-loop safety checks for risky operations.
- Developed an interactive Streamlit UI with chat, knowledge base, file assistant and trace viewer pages.
```

中文版：

```text
- 基於 Python 和 Streamlit 構建可視化多功能 AI Agent 平台，支持文件分析、代碼理解、研究總結、數據分析和任務規劃。
- 設計並實現工具調用 Agent Loop，支持文件讀寫、Shell 命令、代碼掃描、文檔解析和報告生成。
- 實現本地 RAG 知識庫，包括文檔解析、文本切分、向量檢索和基於上下文的答案生成。
- 加入工具調用追蹤、人類確認機制和安全攔截，提高 Agent 執行過程的可觀測性和安全性。
```

---

## 24. 進階升級方向

### 24.1 FastAPI + React 重構

後端：

```text
FastAPI
WebSocket
REST API
SQLite
Agent Service
```

前端：

```text
React
TailwindCSS
Chat UI
Trace Timeline
File Manager
Knowledge Base UI
```

### 24.2 多 Agent 協作

可以加入：

```text
Planner Agent
Research Agent
Code Agent
File Agent
Data Agent
Reviewer Agent
```

流程：

```text
用戶任務 -> Planner 拆解 -> 專業 Agent 執行 -> Reviewer 檢查 -> 最終輸出
```

### 24.3 MCP 工具接入

MCP 可以理解成標準化工具接口，可以把文件系統、資料庫、瀏覽器、GitHub、Notion 等外部服務接入 Agent。

### 24.4 長期記憶

可以保存：

```text
用戶偏好
常用語言
常用項目路徑
歷史任務
常見錯誤
已生成報告
```

存儲方案：

```text
短期：session_state
中期：SQLite
長期：向量數據庫 + metadata
```

### 24.5 權限系統

加入：

```text
只讀模式
安全模式
開發者模式
Shell 禁用模式
高風險命令確認
文件修改 diff 預覽
```

---

## 25. 常見問題與解決方案

### 問題 1：LLM 輸出的 JSON 不合法

解決：

```text
1. prompt 中強調只能輸出 JSON
2. 用 try-except 捕獲 JSONDecodeError
3. 失敗時要求 LLM 重新格式化
4. 後期可以用 Pydantic 做結構校驗
```

### 問題 2：Agent 亂調工具

解決：

```text
1. 工具描述要清晰
2. 每個工具只做一件事
3. 加入工具使用條件
4. 高風險工具默認關閉
5. 加入 human-in-the-loop 確認
```

### 問題 3：RAG 回答不準

解決：

```text
1. 調整 chunk_size
2. 加 overlap
3. 檢索 top_k 不要太少
4. 回答時要求引用檢索片段
5. 加 rerank 模塊
```

### 問題 4：Streamlit 每次刷新狀態丟失

解決：

```text
1. 使用 st.session_state 保存短期狀態
2. 使用 JSON / SQLite 保存長期狀態
3. 將任務、trace、memory 寫入本地文件
```

### 問題 5：Windows 路徑報錯

解決：

```text
1. 優先用 pathlib.Path
2. 不要手寫大量反斜杠
3. 文件路徑用相對 workspace
4. Conda 環境與項目代碼分開
```

---

## 26. 最推薦的 MVP 範圍

第一版不要做太大，控制在：

```text
1. Streamlit 可視化聊天界面
2. 多 Agent 模式選擇
3. 文件上傳與總結
4. 文件讀寫工具
5. 本地知識庫 RAG
6. 代碼項目掃描
7. CSV / Excel 分析
8. 工具調用 Trace
9. 基本安全控制
10. README + Demo
```

這已經足夠作為一個高質量簡歷項目。

---

## 27. 面試時可以這樣講

```text
我做了一個可視化多功能 Agent 平台，目標不是單純聊天，而是讓 Agent 能夠理解任務、調用工具、處理文件、分析代碼、構建本地知識庫並生成報告。

系統核心是 Agent Loop，包含任務理解、工具決策、工具執行、結果觀察和最終回答。為了提高可控性，我設計了 Tool Router、Trace Logger 和安全檢查機制。

在 RAG 模塊中，我實現了文檔解析、文本切分、向量檢索和基於上下文的答案生成。可視化方面，我用 Streamlit 搭建了多頁面界面，包括 Chat、File Assistant、Knowledge Base、Code Assistant、Data Assistant 和 Tool Trace。
```

---

## 28. 最終建議

你現在最適合做的不是「只會幫你寫機器學習報告的 Agent」，而是一個：

```text
面向學習、開發、研究、文件處理、數據分析和任務規劃的可視化通用 Agent 平台
```

最佳路線：

```text
第一版：Streamlit 快速做出可視化效果
第二版：加入 Tool Calling、Trace、File/Data/Code Assistant
第三版：加入 RAG、本地知識庫、Memory
第四版：重構為 FastAPI + React
第五版：加入多 Agent、MCP、權限系統和部署
```

如果你能完成基礎版並配好 README、截圖和 Demo，這會比普通機器學習小 demo 更有競爭力，因為它同時展示了 LLM Agent 工程、RAG、可視化產品、數據處理和安全設計能力。

---

## 29. 參考資料

- OpenAI Agents SDK 官方文檔：Tools、handoffs、tracing、MCP 等 Agent 工程能力。
- LangGraph 官方文檔：適合 long-running、stateful workflow 和 Agent 工作流。
- Streamlit 官方文檔：支持 chat elements、多頁面應用和快速可視化。
- FastAPI 官方文檔：支持高性能 API 和 WebSocket。
