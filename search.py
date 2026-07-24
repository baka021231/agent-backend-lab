from pathlib import Path

def count_keywords(text: str, keywords: list[str]) -> dict[str, int]:
    dic = {keyword : 0 for keyword in keywords}
    for word in text.lower().split():
        word = word.strip(".,!?;:")
        if word in dic:
            dic[word] += 1
    return dic

def load_documents(folder: str) -> dict[str, str]:
    documents = {}
    for file_path in Path(folder).glob("*.md"):
        documents[file_path.name] = file_path.read_text(encoding="UTF-8")
    return documents

def search_documents(query: str, documents: dict[str, str]) -> list[tuple[str, int]]:
    # return most relavent documents and score. e.g.("agent.md", 3)
    if documents == {}: return []

    query_words = [word.strip(".,!?;:") for word in query.lower().split()]

    scores = {}
    for k, v in documents.items():
        count = count_keywords(v, query_words)
        scores[k] = sum(count.values())

    max_value = max(scores.values())

    if max_value == 0: return []

    all_best_pairs = [(k, v) for k, v in scores.items() if v == max_value]
    return all_best_pairs