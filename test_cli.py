import subprocess
import sys


def run_cli(user_input):
    return subprocess.run(
        [sys.executable, "main.py"],
        input=user_input,
        text=True,
        capture_output=True,
    )


def check_cli(name, user_input, expected_texts):
    result = run_cli(user_input)

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr, result.stderr

    for expected_text in expected_texts:
        assert expected_text in result.stdout, result.stdout

    print(f"[PASS] {name}")


# 连续执行两次搜索，然后退出
check_cli(
    name="continuous search",
    user_input="python agent\ndocker container\nexit\n",
    expected_texts=[
        "python.md",
        "docker.md",
        "已退出搜索程序",
    ],
)

# 搜索不存在的关键词
check_cli(
    name="no matching document",
    user_input="elephant\nexit\n",
    expected_texts=[
        "没有找到匹配文档",
        "已退出搜索程序",
    ],
)

# 空输入后继续运行
check_cli(
    name="empty query",
    user_input="\nexit\n",
    expected_texts=[
        "查询不能为空",
        "已退出搜索程序",
    ],
)

# 带空格和大写的退出命令
check_cli(
    name="normalized exit",
    user_input=" EXIT \n",
    expected_texts=[
        "已退出搜索程序",
    ],
)

# 没有任何输入，模拟 EOF
check_cli(
    name="EOF",
    user_input="",
    expected_texts=[
        "已退出搜索程序",
    ],
)

print("All CLI tests passed!")