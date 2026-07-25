# Agent Backend Lab

## 项目目的

本项目从关键词文档检索起步，逐步发展为可测试的 Agent/AI 后端项目。

## 当前真实功能

- 加载指定目录第一层的 Markdown 文档。
- 将文本转为小写，并去除单词首尾的简单标点。
- 统计查询关键词在文档中的出现次数。
- 根据关键词总匹配次数计算文档相关性分数。
- 返回得分最高的文档。
- 最高分相同时返回全部并列文档。
- 没有匹配或没有文档时返回空列表。

## 当前项目结构

```text
agent-backend-lab/
├── README.md
├── main.py
├── search.py
├── test_main.py
├── test_search.py
└── documents/
    ├── agent.md
    ├── docker.md
    └── python.md
```

- `main.py`：当前搜索演示入口。
- `search.py`：文档加载、关键词计数和搜索逻辑。
- `test_main.py`：重构前的关键词计数测试，当前导入路径已失效。
- `test_search.py`：当前搜索场景的自定义测试脚本。
- `documents/`：搜索演示与测试使用的固定语料。

## 运行方法

需要支持 `list[str]` 等类型标注的 Python 版本。在项目目录运行：

```bash
python3 main.py
```

当前演示会从 `documents/` 加载文档并执行 `python agent` 查询。

## 测试方法

分别运行现有测试脚本，并检查输出与进程退出状态：

```bash
python3 test_main.py
python3 test_search.py
```

## 当前测试状态

- `test_search.py` 的 7 个场景显示通过。
- `test_main.py` 因仍从 `main` 导入 `count_keywords` 而失败；该函数目前位于 `search.py`。
- `test_search.py` 是自定义测试脚本，出现失败或异常时不会主动返回非零退出状态，因此不能仅凭进程退出状态可靠判断测试是否失败。

## 当前限制

- 只读取指定目录第一层的 Markdown 文件，不递归读取。
- 相关性只基于关键词出现次数。
- 归一化仅处理小写和有限的首尾标点。
- 当前没有 Web API、LLM、RAG、Agent、数据库或 Docker。

## 后续计划概览

后续拟依次完善可靠测试与命令行交互，再学习和实现 AI 后端、RAG、单 Agent 与工程化能力。具体里程碑和状态以 `project-context/ROADMAP.md` 为准。
