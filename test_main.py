from main import count_keywords

assert count_keywords(
    "python can build agent, and agent needs python",
    ["python", "agent", "docker"]
) == {"python": 2, "agent": 2, "docker": 0}

assert count_keywords(
    "Python PYTHON python.",
    ["python"]
) == {"python": 3}

assert count_keywords(
    "",
    ["python"]
) == {"python": 0}

assert count_keywords(
    "agent, agent! agent?",
    ["agent"]
) == {"agent": 3}

print("All tests passed!")