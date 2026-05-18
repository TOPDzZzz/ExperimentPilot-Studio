# ExperimentPilot Studio

​                             一个可视化的多用途 AI Agent 平台，支持工具调用、RAG、记忆、文件处理、代码分析和任务规划。

## 功能特性

- **可视化聊天界面** — 基于 Streamlit 的多页面 UI，实时展示思考过程
- **工具调用 Agent 循环** — LLM 自主选择并执行工具，逐步追踪执行过程
- **18 个内置工具** — 文件读写、Shell 命令、代码扫描、CSV/Excel 分析、ML 实验报告、网页搜索、报告生成
- **多 Agent 模式** — 通用、文件、代码、数据、ML 实验、研究助手
- **本地 RAG 知识库** — 文档解析、分块、向量检索 (ChromaDB) 和上下文问答
- **记忆系统** — 跨会话持久化用户偏好和近期任务
- **工具追踪查看器** — 实时可视化每个工具调用的输入/输出
- **CLI + Web** — 交互式终端模式 (Typer + Rich) 和 Streamlit Web 界面
- **人机协作安全** — 工作区沙箱、危险命令拦截、路径遍历保护
- **国际化支持** — 中英文界面切换

## 快速开始

### 1. 环境配置

```bash
conda create -n experiment-pilot python=3.11
conda activate experiment-pilot
pip install -r requirements.txt
```

### 2. 配置 API

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 配置：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
```

支持 OpenAI、SiliconFlow 或任何兼容 OpenAI 格式的 API。

### 3. 启动 Web 界面

```bash
streamlit run app.py
```

打开浏览器访问 `http://localhost:8501`

### 4. 使用 CLI

```bash
# 交互式聊天
python cli/main.py chat -m general

# 单次任务执行
python cli/main.py run "analyze experiments/metrics.json" -m ml

# 列出所有工具
python cli/main.py tools
```

## 项目结构

```
ExperimentPilot/
├── app.py                     # Streamlit 主页面
├── cli/main.py                # CLI 入口 (Typer + Rich)
├── pages/                     # Streamlit 多页面 UI
│   ├── 1_💬_Chat_Agent.py
│   ├── 2_📁_File_Assistant.py
│   ├── 3_💻_Code_Assistant.py
│   ├── 4_📊_Data_Assistant.py
│   ├── 5_📚_Knowledge_Base.py
│   ├── 6_🧭_Tool_Trace.py
│   └── 7_⚙️_Settings.py
├── expilot/
│   ├── core/                  # 核心模块 (CLI & Web 共用)
│   │   ├── agent.py           # Agent 循环 (generator 模式)
│   │   ├── llm.py             # LLM 客户端 (带重试)
│   │   ├── memory.py          # 持久化记忆
│   │   ├── trace.py           # 执行追踪日志
│   │   ├── prompts.py         # 提示词模板
│   │   └── schema.py          # 数据模型 (Pydantic)
│   ├── tools/                 # 18 个内置工具
│   ├── rag/                   # RAG 管道
│   │   ├── loader.py          # 文档解析器 (PDF/DOCX/CSV/TXT)
│   │   ├── splitter.py        # 文本分块
│   │   ├── vector_store.py    # ChromaDB 向量存储
│   │   └── retriever.py       # 上下文检索器
│   ├── i18n.py                # 国际化支持
│   └── storage/               # 持久化数据
├── workspace/                 # Agent 沙箱目录
├── experiments/               # ML 实验数据
└── uploads/                   # 用户上传文件
```

## 工具系统

| 类别 | 工具 |
|------|------|
| 文件操作 | `list_dir`, `read_file`, `write_file`, `search_files` |
| Shell | `run_shell` (沙箱化) |
| 代码分析 | `scan_code_project`, `read_code_file` |
| 数据分析 | `analyze_csv`, `analyze_excel` |
| ML 实验 | `summarize_json_metrics`, `compare_experiment_results`, `generate_experiment_report` |
| 报告生成 | `generate_markdown_report`, `generate_html_report`, `save_text_output` |
| 网络工具 | `fetch_url`, `search_web`, `download_file` |

## 使用示例

### 与 Agent 聊天

```
Task > 扫描 workspace 目录并总结项目结构
  Step 1: Using list_dir...
  Step 2: Using read_file...
  Answer: [Markdown 格式的项目结构总结]
```

### ML 实验分析

```
Task > 比较 experiments/metrics.json 和 metrics_baseline.json
  Step 1: Using read_file...
  Step 2: Using compare_experiment_results...
  Answer: [详细的对比分析报告]
```

## 技术栈

- **前端**: Streamlit
- **后端**: Python 3.11
- **LLM**: OpenAI 兼容 API (OpenAI / SiliconFlow / 本地模型)
- **向量数据库**: ChromaDB
- **CLI**: Typer + Rich
- **数据处理**: Pandas, pypdf, python-docx
- **数据校验**: Pydantic

## 开发路线

- [ ] WebSocket 流式输出，实现实时 Token 生成
- [ ] 多 Agent 协作 (规划 → 执行 → 审查)
- [ ] FastAPI + React 生产级重构
- [ ] Docker 容器化部署
- [ ] MCP 工具集成
- [ ] 权限系统 (只读 / 安全 / 开发者模式)

## 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。
