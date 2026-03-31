# DevMate

DevMate 是一个基于 **LangChain** 构建的智能编程 Agent，目标是帮助开发者完成代码生成、代码修改、知识检索与工具调用等任务。

本项目用于完成 AI Agent 面试任务，当前已完成基础工程搭建、模型配置接入与 LangSmith 可观测性验证，后续将继续补齐 RAG、MCP、Skills、Docker 和端到端 Agent 主循环。

---

## Features

### 已完成
- 使用 `uv` 管理依赖与运行环境
- 使用 `pyproject.toml` 管理项目
- Python `3.13`
- 基于 `config.toml` 的配置管理
- 支持主模型 / Embedding 模型 / 规划模型配置
- 基于 LangChain 的模型初始化
- 集成 LangSmith，可正常查看 Trace
- 完成基础 smoke test

### 计划中
- RAG：本地 markdown / text 文档索引与检索
- MCP Server / MCP Client
- 基于 **Streamable HTTP** 的 Tavily 搜索接入
- Agent 主循环：规划、工具调用、代码生成与修改
- Skills 技能系统（默认目录 `.skills`）
- Docker / docker-compose
- 端到端场景验证

---

## Requirements

- Python 3.13
- `uv`
- 可用的大模型 API Key
- LangSmith API Key
- （后续）Tavily API Key

---

## Quick Start

### 1. 安装依赖

```bash
uv sync
```

### 2. 检查 Python 版本

```bash
uv run python --version
```

### 3. 配置 `config.toml`

在项目根目录创建或修改 `config.toml`：

```toml
[model]
ai_base_url = "https://your-openai-compatible-endpoint/v1"
api_key = "REPLACE_ME"
model_name = "your-chat-model"
embedding_model_name = "your-embedding-model"
planner_model_name = "your-planner-model"
temperature = 0.1
max_tokens = 8192

[search]
tavily_api_key = "REPLACE_ME"
max_results = 5

[langsmith]
langchain_tracing_v2 = true
langchain_api_key = "REPLACE_ME"
project = "devmate"
endpoint = "https://api.smith.langchain.com"

[skills]
skills_dir = ".skills"

[rag]
docs_dir = "docs"
vector_store_dir = ".data/vector_store"
chunk_size = 1000
chunk_overlap = 200
top_k = 4
```

### 4. 运行基础测试

```bash
uv run python devmate/test.py --prompt "请用一句话介绍 DevMate 当前状态"
```

---

## Observability

项目已集成 **LangSmith**，当前已验证：

- Trace 可以成功上报
- 可在 LangSmith 后台查看运行记录
- 后续将进一步补齐 Agent、RAG、MCP 工具调用链路的完整追踪

---

## Project Structure

```text
DevMate/
├─ devmate/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ llm.py
│  ├─ observability.py
│  └─ ...
├─ config.toml
├─ pyproject.toml
└─ README.md
```

---

## Current Status

当前项目已完成第一阶段基础能力建设，包括：

- 工程初始化
- 配置系统
- 模型初始化
- LangSmith 可观测性打通

其中 **LangSmith Trace 已可正确显示**，说明基础调用链路与观测链路已具备可验证性。

---

## Roadmap

后续将按以下顺序推进：

1. **RAG**
   - 解析并索引本地 markdown/text 文档
   - 建立向量数据库
   - 提供 `search_knowledge_base(query)` 工具

2. **MCP**
   - 实现 MCP Server
   - 使用 **Streamable HTTP**
   - 通过 MCP Client 调用 Tavily 搜索工具 `search_web`

3. **Agent**
   - 接收用户输入
   - 自主规划
   - 自主判断是否查网络 / 查知识库
   - 调用工具
   - 生成或修改代码文件

4. **Skills**
   - 学习、存储和复用成功任务模式
   - 默认目录 `.skills`

5. **Docker**
   - 提供 `Dockerfile`
   - 提供 `docker-compose.yml`

---

## Notes

- 不使用 `requirements.txt`
- 所有配置通过 `config.toml` 管理
- 所有 Python 代码需遵守 **PEP 8**
- 日志统一使用 `logging`，不使用 `print()`