import subprocess
import sys
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import json


def run_cli_process(user_input, log_path):
    env = os.environ.copy()
    env["SEARCH_LOG_PATH"] = str(log_path)

    test_entry = (
        "from main import run_cli; "
        "from llm_client import MyClient; "
        "run_cli(MyClient())"
    )

    return subprocess.run(
        [sys.executable, "-c", test_entry],
        input=user_input,
        text=True,
        capture_output=True,
        env = env
    )


def check_cli(name, user_input, expected_texts, expected_queries, expected_results):
    with TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "logs" / "events.jsonl"
        result = run_cli_process(user_input, log_path)

        assert result.returncode == 0, result.stderr
        assert "Traceback" not in result.stderr, result.stderr

        for expected_text in expected_texts:
            assert expected_text in result.stdout, result.stdout

        expected_llm_calls = sum(
        bool(search_results)
        for search_results in expected_results
        )
        actual_llm_calls = result.stdout.splitlines().count("Hello")

        assert actual_llm_calls == expected_llm_calls

        if log_path.exists():
            lines = log_path.read_text(encoding="utf-8").splitlines()
            events = [json.loads(line) for line in lines]
        else:
            events = []
        actual_queries = [
            event["query"] for event in events
        ]
        actual_results = [
            event["results"] for event in events
        ]

        assert actual_queries == expected_queries
        assert actual_results == expected_results
        assert all(
            isinstance(event["elapsed_ms"], (int, float))
            and event["elapsed_ms"] >= 0
            for event in events
        )

        print(f"[PASS] {name}")

def check_log_failure():
    with TemporaryDirectory() as temp_dir:
        log_path = Path(temp_dir) / "not_a_file"
        log_path.mkdir()

        result = run_cli_process(
            "python agent\nexit\n",
            log_path,
        )

        assert result.returncode == 0
        assert "python.md" in result.stdout
        assert "写入搜索日志失败" in result.stderr
        assert "Traceback" not in result.stderr

        print("[PASS] log write failure")


# 连续执行两次搜索，然后退出
check_cli(
    name="continuous search",
    user_input="python agent\ndocker container\nexit\n",
    expected_texts=[
        "python.md",
        "docker.md",
        "已退出搜索程序",
    ],
    expected_queries=[
        "python agent",
        "docker container",
    ],
    expected_results=[
        [
            {"filename": "python.md", "score": 4}
        ],
        [
            {"filename": "docker.md", "score": 2}
        ]
    ]
)

# 搜索不存在的关键词
check_cli(
    name="no matching document",
    user_input="elephant\nexit\n",
    expected_texts=[
        "没有找到匹配文档",
        "已退出搜索程序",
    ],
    expected_queries=["elephant"],
    expected_results=[[]],
)

# 空输入后继续运行
check_cli(
    name="empty query",
    user_input="\nexit\n",
    expected_texts=[
        "查询不能为空",
        "已退出搜索程序",
    ],
    expected_queries=[],
    expected_results=[],
)

# 带空格和大写的退出命令
check_cli(
    name="normalized exit",
    user_input=" EXIT \n",
    expected_texts=[
        "已退出搜索程序",
    ],
    expected_queries=[],
    expected_results=[],
)

# 没有任何输入，模拟 EOF
check_cli(
    name="EOF",
    user_input="",
    expected_texts=[
        "已退出搜索程序",
    ],
    expected_queries=[],
    expected_results=[],
)

check_log_failure()

print("All CLI tests passed!")