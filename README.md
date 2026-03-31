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
uv run python devmate/scripts/test.py --prompt "请用一句话介绍 DevMate 当前状态"
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
├─ scripts/
│  ├─ test.py
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
# DevMate - 第二阶段 README（MCP 实现）

## 阶段目标

第二阶段的目标是为 DevMate 实现基于 **MCP（Model Context Protocol）** 的网络搜索能力，使 Agent 可以通过标准化协议访问外部搜索工具，而不是直接把搜索逻辑硬编码在主应用中。

根据项目要求，本阶段需要满足以下硬性条件：

- 实现至少一个 **MCP Server**
- 实现至少一个 **MCP Client**
- MCP 传输方式必须使用 **Streamable HTTP**
- 不接受 `stdio` 或 `SSE`
- 搜索服务必须使用 **Tavily**
- Agent 必须通过 MCP 调用 `search_web`

---

## 本阶段对应需求

本阶段主要对应以下要求：

### requirements.md
- 必须实现 MCP 能力
- 至少一个 MCP Server
- 至少一个 MCP Client
- MCP 必须使用 **Streamable HTTP**
- 搜索服务必须使用 **Tavily**
- Agent 通过 MCP 调用搜索工具 `search_web`

### checklist.md
- 第二阶段: MCP 实现（网络搜索）
- 实现一个基本的 MCP server，暴露 `search_web` 工具
- 集成 Tavily Search API
- 验证 server 正常运行并通过 Streamable HTTP 提供服务
- 在主应用程序中实现一个 MCP client
- 将 client 通过 Streamable HTTP 连接到 MCP server
- 运行手动测试，确保 Agent 成功调用搜索工具并返回结果

---

## 设计思路

本阶段采用如下设计：

### 1. MCP Server
MCP Server 负责暴露统一工具接口：

- `search_web(query: str)`

该工具内部调用 Tavily Search API，返回搜索结果摘要。

### 2. MCP Client
主应用中的 MCP Client 负责：

- 通过 **Streamable HTTP** 连接 MCP Server
- 获取工具列表
- 调用 `search_web`
- 将结果交给 Agent 继续推理

### 3. 为什么要这么设计
这样做有几个好处：

- 搜索能力和 Agent 主流程解耦
- 网络搜索能力可独立测试
- 后续可以在不改主 Agent 的情况下替换搜索实现
- 更符合 MCP 生态和面试任务要求

### 4. 运行命令

```bash
uv run devmate-run-mcp-server
uv run --no-sync devmate-test-mcp-client
```
## 第三阶段实现

结合当前开发过程，本阶段已经完成了一个最小可运行版本（MVP），实现流程如下：

### 1. 文档数据准备
在项目中创建了 `docs/` 目录，并添加了本地知识文档，例如：

- `docs/project_guidelines.md`
- `docs/internal_fastapi_guidelines.md`

这些文件用于模拟内部项目规范、后端开发约束和默认工程结构。

### 2. 文档读取
RAG 模块会递归读取 `docs/` 目录下的 `.md` 文件。

为了避免 Windows 环境下默认编码导致的报错，读取过程采用了显式 UTF-8 编码方式：

- 使用 `Path.rglob("*.md")` 遍历文件
- 使用 `read_text(encoding="utf-8")` 读取内容

这样避免了 `gbk` 默认解码造成的 `UnicodeDecodeError`

### 3. 文本切分
读取后的文档会使用 `RecursiveCharacterTextSplitter` 切分成多个 chunk，以便后续生成向量并提升检索命中率。

### 4. 嵌入生成
使用配置中的 embedding 模型生成向量。

当前日志显示 embedding 链路工作正常，例如：

- 模型：`Pro/BAAI/bge-m3`
- 向量维度：`1024`

### 5. 向量存储
向量数据库使用 **Chroma**，本地持久化目录为：

```text
.chroma
```
### 4. 运行命令

```bash
uv run --no-sync devmate-test-rag
```

## Roadmap

后续将按以下顺序推进：


1. **Agent**
   - 接收用户输入
   - 自主规划
   - 自主判断是否查网络 / 查知识库
   - 调用工具
   - 生成或修改代码文件

2. **Skills**
   - 学习、存储和复用成功任务模式
   - 默认目录 `.skills`

3. **Docker**
   - 提供 `Dockerfile`
   - 提供 `docker-compose.yml`

---

## Notes

- 不使用 `requirements.txt`
- 所有配置通过 `config.toml` 管理
- 所有 Python 代码需遵守 **PEP 8**
- 日志统一使用 `logging`，不使用 `print()`