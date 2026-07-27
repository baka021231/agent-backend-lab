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
- 从项目 `.env` 中读取 `DEEPSEEK_API_KEY`，调用 DeepSeek Chat Completions。
- 将用户问题和命中文档构造成限定上下文的提示词。
- 在 CLI 展示检索结果后输出基于命中文档的模型回答。
- CLI 自动化测试使用替身客户端，不发送真实 API 请求。

## 当前项目结构

```text
agent-backend-lab/
├── documents/
│   ├── agent.md
│   ├── docker.md
│   └── python.md
├── event_log.py
├── llm_client.py
├── main.py
├── prompt_builder.py
├── README.md
├── search.py
├── test_cli.py
├── test_event_log.py
├── test_llm_client.py
├── test_prompt_builder.py
└── test_search.py
```

- `main.py`：连续命令行入口，负责检索、计时、事件记录、提示词构造和模型回答。
- `search.py`：文档加载、关键词计数和搜索逻辑。
- `event_log.py`：构建搜索事件并以 JSONL 格式追加写入。
- `llm_client.py`：定义 `LLMClient` 协议、离线替身和 DeepSeek 客户端。
- `prompt_builder.py`：把查询和命中文档构造成模型提示词。
- `test_search.py`：搜索逻辑测试。
- `test_event_log.py`：事件构建、JSON 序列化和 JSONL 追加测试。
- `test_llm_client.py`：替身客户端烟雾检查。
- `test_prompt_builder.py`：提示词内容、文档过滤和无匹配行为测试。
- `test_cli.py`：使用替身客户端验证连续查询、模型调用次数、退出边界和日志失败处理。
- `documents/`：搜索演示与测试使用的固定语料。

## 运行方法

需要 Python 3.10 或更高版本。在项目目录创建并激活虚拟环境，然后安装当前依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install openai python-dotenv
```

在项目根目录创建 `.env`，填入自己的 Key：

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

## 查询日志

每次有效查询默认追加到 `logs/search_events.jsonl`。每行都是一个独立 JSON 对象：

```json
{"timestamp":"2026-07-26T00:00:00+00:00","query":"python agent","results":[{"filename":"python.md","score":4}],"elapsed_ms":0.1}
```

字段含义：

- `timestamp`：UTC 时区的 ISO 8601 时间。
- `query`：归一化后的查询文本。
- `results`：最高分文档及其分数；无匹配时为空列表。
- `elapsed_ms`：搜索计算耗时，单位为毫秒。

可通过环境变量将日志写入其他路径：

```bash
SEARCH_LOG_PATH=/tmp/search-events.jsonl python3 main.py
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
```

这些测试不会调用真实 DeepSeek；真实 API 调用只用于手动冒烟验证。

## 当前测试状态

- 搜索测试覆盖 7 个场景。
- 事件日志测试覆盖连续追加、UTF-8 文本和逐行 JSON 解析。
- 提示词测试覆盖查询、命中文档过滤和无匹配行为。
- CLI 测试使用替身客户端，覆盖连续搜索、模型调用次数、无匹配、空输入、标准化退出、EOF 和日志写入失败。
- 断言失败或出现未处理异常时，测试脚本会以非零状态退出。

## 当前限制

- 只读取指定目录第一层的 Markdown 文件，不递归读取。
- 相关性只基于关键词出现次数。
- 归一化仅处理小写和有限的首尾标点。
- 尚未实现中文分词、文档切块、Embedding 或向量检索。
- 正式 CLI 尚未捕获缺少 Key、模型调用失败和空响应等 LLM 异常。
- 尚未实现 API 重试、限流或缓存。
- JSONL 日志暂未实现轮转、并发写入、重试或备用路径。
- 当前没有 Web API、Agent、数据库或 Docker。

## 后续计划概览

后续将继续学习和实现 AI 后端、RAG、单 Agent 与工程化能力。具体里程碑和状态以 `project-context/ROADMAP.md` 为准。
