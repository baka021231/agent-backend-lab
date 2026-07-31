from pydantic import BaseModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from search import load_documents

class Chunk(BaseModel):
    text: str
    source: str
    chunk_index: int
    chunk_id: str

def chunk_document(
        source: str,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    pieces = splitter.split_text(text)

    chunk_list = []
    for index, value in enumerate(pieces):
        chunk_list.append(Chunk(text=value, source=source, chunk_index=index, chunk_id=f"{source}:{index}"))

    return chunk_list

def chunk_documents(
    documents: dict[str, str],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    chunk_list = []
    for key, value in documents.items():
        chunk_list.extend(chunk_document(source=key, text=value, chunk_size=chunk_size, chunk_overlap=chunk_overlap))
    return chunk_list

def load_chunks(
    folder: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Chunk]:
    return chunk_documents(load_documents(folder=folder), chunk_size=chunk_size, chunk_overlap=chunk_overlap)