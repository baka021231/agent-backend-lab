from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel

from chunking import Chunk
from llm_client import LLMClient
from prompt_builder import build_chunk_prompt
from vector_retriever import retrieve


class RAGAnswer(BaseModel):
    answer: str
    sources: list[Chunk]


def answer_question(
    query: str,
    store: InMemoryVectorStore,
    client: LLMClient,
    k: int = 3,
) -> RAGAnswer | None:
    chunks = retrieve(query=query, store=store, k=k)
    prompt = build_chunk_prompt(query=query, chunks=chunks)
    if prompt is None:
        return None
    answer = client.generate(prompt=prompt)
    return RAGAnswer(answer=answer, sources=chunks)