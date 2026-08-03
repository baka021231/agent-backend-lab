import json
from pathlib import Path
from search import search_documents
from vector_retriever import retrieve, InMemoryVectorStore

def hit_at_1(retrieved_sources: list[str], expected_sources: list[str]) -> int:
    if not retrieved_sources:
        return 0
    if retrieved_sources[0] in expected_sources:
        return 1
    else:
        return 0

def load_eval_samples(path: str) -> list[dict]:
    context = Path(path).read_text(encoding='utf-8')
    samples = []
    for line in context.splitlines():
        samples.append(json.loads(line))
    return samples

def keyword_retrieve_sources(
    query: str,
    documents: dict[str, str],
) -> list[str]:
    res = search_documents(query=query, documents=documents)
    if not res: return []
    return [item[0] for item in res]

def evaluate_keyword_baseline(
    samples: list[dict],
    documents: dict[str, str],
) -> dict:
    res = {
    "method": "keyword",
    "sample_count": len(samples),
    "hits": 0,
    "hit_at_1": 0,
    "results": [
    ]
}
    for sample in samples:
        query = sample["query"]
        hit_docs = keyword_retrieve_sources(query=query, documents=documents)
        hits = hit_at_1(retrieved_sources=hit_docs, expected_sources=sample["expected_sources"])
        res["hits"] += hits
        res["results"].append({"query": query, "expected_sources": sample["expected_sources"], "category": sample["category"], "retrieved_sources": hit_docs, "hit": hits})
    res["hit_at_1"] = (res["hits"] / res["sample_count"] if res["sample_count"] else 0.0)
    return res

def vector_retrieve_sources(
    query: str,
    store: InMemoryVectorStore,
) -> list[str]:
    chunks = retrieve(query=query, store=store, k=1)
    return list(dict.fromkeys(chunk.source for chunk in chunks))

def evaluate_vector_baseline(
    samples: list[dict],
    store: InMemoryVectorStore,
) -> dict:
    res = {
    "method": "vector",
    "sample_count": len(samples),
    "hits": 0,
    "hit_at_1": 0,
    "results": [
    ]
}
    for sample in samples:
        query = sample["query"]
        hit_docs = vector_retrieve_sources(query=query, store=store)
        hits = hit_at_1(retrieved_sources=hit_docs, expected_sources=sample["expected_sources"])
        res["hits"] += hits
        res["results"].append({"query": query, "expected_sources": sample["expected_sources"], "category": sample["category"], "retrieved_sources": hit_docs, "hit": hits})
    res["hit_at_1"] = (res["hits"] / res["sample_count"] if res["sample_count"] else 0.0)
    return res