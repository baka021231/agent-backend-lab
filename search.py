from pathlib import Path

def load_documents(folder):
    documents = {}
    for file_path in Path(folder).glob("*.md"):
        documents[file_path.name] = file_path.read_text(encoding="UTF-8")
    return documents

if __name__ == "__main__":
    documents = load_documents("documents")

    assert len(documents) == 3
    assert "python.md" in documents
    assert "agent.md" in documents
    assert "docker.md" in documents

    for filename, content in documents.items():
        print(filename, len(content))

    print("All documents loaded!")