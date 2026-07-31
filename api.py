from pydantic import BaseModel
from search import load_documents, search_documents
from fastapi import FastAPI, HTTPException, Depends
from langchain_core.vectorstores import InMemoryVectorStore

from llm_client import LLMClient, LLMClientError
from rag_service import RAGAnswer, answer_question

class AskRequest(BaseModel):
    query: str
    k: int = 3

app = FastAPI()

def configure_rag(
    store: InMemoryVectorStore,
    client: LLMClient,
) -> None:
    app.state.vector_store = store
    app.state.llm_client = client

def get_vector_store() -> InMemoryVectorStore:
    store = getattr(app.state, "vector_store", None)
    if store is None:
        raise HTTPException(status_code=503, detail="RAG service is not configured")
    return store

def get_llm_client() -> LLMClient:
    client = getattr(app.state, "llm_client", None)
    if client is None:
        raise HTTPException(status_code=503, detail="RAG service is not configured")
    return client

@app.get("/health")
def health() -> dict[str, str]:
    return {"status" : "ok"}

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    filename: str
    score: int

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    query = request.query.strip().lower()
    if query == "":
        raise HTTPException(status_code=422, detail="query must not be blank")
    try:
        documents = load_documents("documents")
    except OSError:
        raise HTTPException(status_code=500, detail="failed to load documents")

    if not documents:
        raise HTTPException(status_code=503, detail="no searchable documents")

    matches = search_documents(documents=documents, query=query)
    res = []
    for match in matches:
        search_res = SearchResult(filename=match[0], score=match[1])
        res.append(search_res)
    return SearchResponse(query=query, results=res)

@app.post("/ask", response_model=RAGAnswer)
def ask(
    request: AskRequest,
    store: InMemoryVectorStore = Depends(get_vector_store),
    client: LLMClient = Depends(get_llm_client),
) -> RAGAnswer:
    query = request.query.strip()
    if query == "" or request.k < 1:
        raise HTTPException(status_code=422)
    try:
        answer = answer_question(query=query, store=store, client=client, k=request.k)
    except LLMClientError as error:
        raise HTTPException(status_code=502, detail="LLM service failed") from error
    if answer is None:
        raise HTTPException(status_code=404, detail="no relevant context")
    return answer