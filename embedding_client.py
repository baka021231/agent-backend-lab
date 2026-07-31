from typing import Protocol

from pydantic import BaseModel

from chunking import Chunk

from sentence_transformers import SentenceTransformer

from langchain_core.embeddings import Embeddings


class EmbeddingClient(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...

class LocalEmbeddingClient(Embeddings):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self._model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vector_list = self._model.encode(texts)
        return vector_list.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._model.encode(text).tolist()


class EmbeddedChunk(BaseModel):
    chunk: Chunk
    vector: list[float]

def embed_chunks(
        chunks: list[Chunk],
        client: EmbeddingClient,
) -> list[EmbeddedChunk]:
    texts = [chunk.text for chunk in chunks]
    vectors = client.embed_documents(texts=texts)
    emb_chunks = []
    for chunk, vector in zip(chunks, vectors):
        emb_chunks.append(EmbeddedChunk(chunk=chunk, vector=vector))
    return emb_chunks
