from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings
from chunking import Chunk


def build_vector_store(
    chunks: list[Chunk],
    client: Embeddings,
) -> InMemoryVectorStore:
    store = InMemoryVectorStore(embedding=client)
    texts = [chunk.text for chunk in chunks]
    ids = [chunk.chunk_id for chunk in chunks]
    metadatas = [chunk.model_dump(exclude={"text"}) for chunk in chunks]
    store.add_texts(texts=texts, ids=ids, metadatas=metadatas)
    return store

def retrieve(
    store: InMemoryVectorStore,
    query: str,
    k: int = 3,
) -> list[Chunk]:
    documents = store.similarity_search(query=query, k=k)
    chunks = []
    for doc in documents:
        chunks.append(Chunk(text=doc.page_content, **doc.metadata))
    return chunks