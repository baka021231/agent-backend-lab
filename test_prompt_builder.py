from prompt_builder import build_prompt

documents = {
    "python.md": "Python emphasizes readability.",
    "docker.md": "Docker runs containers.",
}

prompt = build_prompt(
    query="什么是 Python？",
    results=[("python.md", 4)],
    documents=documents,
)

assert prompt is not None
assert "什么是 Python？" in prompt
assert "python.md" in prompt
assert "Python emphasizes readability." in prompt
assert "Docker runs containers." not in prompt

assert build_prompt(
    query="不存在的问题",
    results=[],
    documents=documents,
) is None