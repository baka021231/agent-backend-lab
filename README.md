# Agent Backend Lab

## 项目目的

本项目从关键词文档检索起步，逐步发展为可测试的 Agent/AI 后端项目。

## 当前真实功能

- 加载 `documents/` 第一层的 Markdown 文档。
- 对查询词进行小写和简单标点归一化。
- 按关键词出现次数计算相关性。
- 返回最高分文档；最高分相同时返回全部并列文档。
- 没有匹配时返回空列表。
- 支持在命令行中连续输入查询。
- 空输入不会执行搜索；输入 `exit` 或 `quit` 可退出程序。
- 每次有效查询都会追加一条 JSONL 事件日志。
- 日志记录 `timestamp`、`query`、`results` 和 `elapsed_ms`。
- 日志写入失败时显示警告，但不会中断搜索程序。
- 通过 `LLMClient` 协议隔离具体模型客户端。
- 从进程环境或项目 `.env` 中读取 `DEEPSEEK_API_KEY`，调用 DeepSeek Chat Completions；已有进程环境变量优先。
- 将用户问题和命中文档构造成限定上下文的提示词。
- 在 CLI 展示检索结果后输出基于命中文档的模型回答。
- CLI 自动化测试使用替身客户端，不发送真实 API 请求。
- 缺少 API Key 时显示明确的启动失败信息并以状态 1 退出。
- 模型调用失败或返回空内容时显示本次回答错误，不输出 Traceback，并允许继续查询。
- 提供最小 FastAPI 应用；`GET /health` 返回状态 200 和 `{"status": "ok"}`，用于确认服务存活，不调用检索或模型。
- 提供关键词版 `POST /search`；接收 JSON 查询，返回规范化后的 query 和命中文档及分数。
- `/search` 对正常命中和无匹配返回 200，空查询返回 422，无可搜索文档返回 503，文档读取失败返回 500。
- 将 Markdown 文档切分为带 `source`、`chunk_index` 和 `chunk_id` 的文本块。
- 使用本地 Sentence Transformer 生成向量，并写入 LangChain 内存向量库。
- 根据问题执行 Top-k 语义检索，并把检索到的来源段落交给模型生成回答。
- 提供 `POST /ask` 的 RAG 接口边界；成功响应同时返回模型回答和完整来源段落。
- `/ask` 对未配置服务、无相关上下文和模型服务失败分别返回 503、404 和 502。

## 当前项目结构

```text
agent-backend-lab/
├── documents/
│   ├── agent.md
│   ├── docker.md
│   └── python.md
├── api.py
├── chunking.py
├── cli_test_clients.py
├── embedding_client.py
├── event_log.py
├── llm_client.py
├── main.py
├── prompt_builder.py
├── rag_service.py
├── README.md
├── search.py
├── test_api.py
├── test_cli.py
├── test_event_log.py
├── test_llm_client.py
├── test_prompt_builder.py
├── test_search.py
└── vector_retriever.py
```

- `main.py`：连续命令行入口，负责检索、计时、事件记录、提示词构造和模型回答。
- `api.py`：FastAPI 应用入口，提供 `GET /health`、关键词版 `POST /search` 和 RAG 版 `POST /ask`。
- `chunking.py`：加载 Markdown 文档，并切分为保留来源和段落位次的 `Chunk`。
- `embedding_client.py`：定义 Embedding 客户端协议、本地模型实现和批量向量化函数。
- `vector_retriever.py`：构建内存向量库并执行 Top-k 语义检索。
- `rag_service.py`：编排检索、提示词构造、模型调用和来源返回。
- `search.py`：文档加载、关键词计数和搜索逻辑。
- `cli_test_clients.py`：为 CLI 离线失败测试提供可替换的模型客户端。
- `event_log.py`：构建搜索事件并以 JSONL 格式追加写入。
- `llm_client.py`：定义 `LLMClient` 协议、离线替身和 DeepSeek 客户端。
- `prompt_builder.py`：把查询和命中文档构造成模型提示词。
- `test_search.py`：搜索逻辑测试。
- `test_api.py`：使用 TestClient 验证 `/health`，以及 `/search` 的正常、无匹配、空查询、无文档和读取失败契约。
- `test_event_log.py`：事件构建、JSON 序列化和 JSONL 追加测试。
- `test_llm_client.py`：缺少 Key、底层调用失败和空响应的离线异常契约检查。
- `test_prompt_builder.py`：提示词内容、文档过滤和无匹配行为测试。
- `test_cli.py`：使用替身客户端验证连续查询、模型调用次数、退出边界、日志失败和 LLM 失败处理。
- `documents/`：搜索演示与测试使用的固定语料。

## 运行方法

需要 Python 3.10 或更高版本。在项目目录创建并激活虚拟环境，然后安装当前依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install openai python-dotenv pytest fastapi uvicorn httpx langchain-core langchain-text-splitters sentence-transformers
```

可以直接设置进程环境变量，也可以在项目根目录创建 `.env` 并填入自己的 Key：

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
```

`.env` 已被 Git 忽略，不应提交。配置完成后运行：

```bash
python main.py
```

程序会加载 `documents/` 中的 Markdown 文件，然后等待查询。每行输入一次查询，例如：

```text
请输入查询词：
python agent
```

程序会先显示命中的文档与分数，再调用 DeepSeek 输出基于命中文档的回答。输入 `exit` 或 `quit` 退出；也可以使用 EOF（通常是 Ctrl+D）或 Ctrl+C 结束程序。

启动 FastAPI 最小服务：

```bash
python -m uvicorn api:app --reload
```

启动后可访问 `http://127.0.0.1:8000/health`。该路由只返回服务存活状态，不需要 DeepSeek API Key，也不会调用搜索或模型。

使用关键词搜索：

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"docker"}'
```

正常响应示例：

```json
{"query":"docker","results":[{"filename":"docker.md","score":1}]}
```

查询会先去除首尾空白并转为小写。无匹配属于成功搜索，返回状态 200 和空 `results`；空查询、无文档和文档读取失败分别返回 422、503 和 500。`/search` 只调用本地关键词检索，不调用 DeepSeek。

## 查询日志

每次有效查询默认追加到 `logs/search_events.jsonl`。每行都是一个独立 JSON 对象：

```json
{"timestamp":"2026-07-26T00:00:00+00:00","query":"python agent","results":[{"filename":"python.md","score":4}],"elapsed_ms":0.1}
```

字段含义：

- `timestamp`：UTC 时区的 ISO 8601 时间。
- `query`：去除首尾空白并转为小写后的查询文本。
- `results`：最高分文档及其分数；无匹配时为空列表。
- `elapsed_ms`：搜索计算耗时，单位为毫秒。

可通过环境变量将日志写入其他路径：

```bash
SEARCH_LOG_PATH=/tmp/search-events.jsonl python main.py
```

如果日志无法写入，程序会向标准错误输出警告，但仍会显示本次搜索结果并允许继续查询。

## 测试方法

分别运行现有离线测试脚本，并同时检查输出和退出状态：

```bash
python test_event_log.py
python test_search.py
python test_llm_client.py
python test_prompt_builder.py
python test_cli.py
python -m pytest test_api.py -v
```

这些测试不会调用真实 DeepSeek；API 测试通过 TestClient 在进程内请求 FastAPI 应用，不需要启动 Uvicorn。真实 API 调用只用于手动冒烟验证。

## 当前测试状态

- 搜索测试覆盖 7 个场景。
- 事件日志测试覆盖连续追加、UTF-8 文本和逐行 JSON 解析。
- 提示词测试覆盖查询、命中文档过滤和无匹配行为。
- LLM 客户端测试覆盖缺少 Key、底层调用失败和模型空响应，且不会发起真实请求。
- CLI 测试共覆盖 9 个场景，包括连续搜索、模型调用次数、无匹配、空输入、标准化退出、EOF、日志写入失败、启动配置失败和两类模型回答失败。
- FastAPI 测试确实请求 `GET /health` 和 `POST /search`；共 6 个 pytest 场景，覆盖健康检查、正常搜索与查询归一化、无匹配、空查询 422、无文档 503 和读取失败 500。
- `/ask` 已使用离线替身验证成功回答与来源返回，以及 422、404、502、503 失败边界；验证不会调用真实模型 API。
- 断言失败或出现未处理异常时，测试脚本会以非零状态退出。
- 当前 FastAPI 0.140.13 组合会产生一条 TestClient/httpx 弃用 warning；测试仍通过，退出状态为 0。

## 当前限制

- 只读取指定目录第一层的 Markdown 文件，不递归读取。
- 相关性只基于关键词出现次数。
- 归一化仅处理小写和有限的首尾标点。
- 当前向量库只存在于进程内，服务重启后需要重新构建。
- `/ask` 已有接口与依赖注入边界，但尚未通过 FastAPI lifespan 在服务启动时自动构建向量库和模型客户端；未调用 `configure_rag` 时会返回 503。
- 当前没有为 `/ask` 提供可直接启动 Uvicorn 的生产配置入口。
- 尚未实现 API 重试、限流或缓存。
- JSONL 日志暂未实现轮转、并发写入、重试或备用路径。
- Web API 尚未实现认证或更完整的业务能力。
- 当前没有 Agent、数据库或 Docker。

## 后续计划概览

后续将继续学习和实现 AI 后端、RAG、单 Agent 与工程化能力。具体里程碑和状态以 `project-context/ROADMAP.md` 为准。
