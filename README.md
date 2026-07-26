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

## 当前项目结构

```text
agent-backend-lab/
├── documents/
│   ├── agent.md
│   ├── docker.md
│   └── python.md
├── event_log.py
├── main.py
├── README.md
├── search.py
├── test_cli.py
├── test_event_log.py
└── test_search.py
```

- `main.py`：连续命令行搜索入口，负责计时、事件记录和交互错误处理。
- `search.py`：文档加载、关键词计数和搜索逻辑。
- `event_log.py`：构建搜索事件并以 JSONL 格式追加写入。
- `test_search.py`：搜索逻辑测试。
- `test_event_log.py`：事件构建、JSON 序列化和 JSONL 追加测试。
- `test_cli.py`：连续查询、退出边界和日志失败处理测试。
- `documents/`：搜索演示与测试使用的固定语料。

## 运行方法

需要 Python 3.9 或更高版本。在项目目录运行：

```bash
python3 main.py
```

程序会加载 `documents/` 中的 Markdown 文件，然后等待查询。每行输入一次查询，例如：

```text
请输入查询词：
python agent
```

输入 `exit` 或 `quit` 退出。也可以使用 EOF（通常是 Ctrl+D）或 Ctrl+C 结束程序。

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

分别运行三个现有测试脚本，并同时检查输出和退出状态：

```bash
python3 test_event_log.py
python3 test_search.py
python3 test_cli.py
```

## 当前测试状态

- 搜索测试覆盖 7 个场景。
- 事件日志测试覆盖连续追加、UTF-8 文本和逐行 JSON 解析。
- CLI 测试覆盖连续搜索、无匹配、空输入、标准化退出、EOF 和日志写入失败。
- 所有测试脚本都使用断言；失败时会以非零状态退出。

## 当前限制

- 只读取指定目录第一层的 Markdown 文件，不递归读取。
- 相关性只基于关键词出现次数。
- 归一化仅处理小写和有限的首尾标点。
- JSONL 日志暂未实现轮转、并发写入、重试或备用路径。
- 当前没有 Web API、LLM、RAG、Agent、数据库或 Docker。

## 后续计划概览

后续将继续学习和实现 AI 后端、RAG、单 Agent 与工程化能力。具体里程碑和状态以 `project-context/ROADMAP.md` 为准。
