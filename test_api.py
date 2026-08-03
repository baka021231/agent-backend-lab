from fastapi.testclient import TestClient
from api import app, get_llm_client, get_vector_store
from rag_service import RAGAnswer
from unittest.mock import patch

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_search_success():
    response = client.post("/search", json={"query" : " Docker "})
    assert response.status_code == 200
    assert response.json() =={
        "query": "docker",
        "results": [{"filename": "docker.md", "score": 1}],
    }

def test_search_no_match():
    response = client.post("/search", json={"query" : "term-that-does-not-exist"})
    assert response.status_code == 200
    assert response.json() == {
        "query": "term-that-does-not-exist",
        "results": [],
    }

def test_search_blank_query():
    response = client.post("/search", json={"query" : ""})
    assert response.status_code == 422
    assert response.json() == {"detail": "query must not be blank"}

def test_search_no_documents():
    with patch("api.load_documents", return_value={}):
        response = client.post("/search", json={"query" : "agent"})
    assert response.status_code == 503
    assert response.json() == {"detail": "no searchable documents"}

def test_search_load_failure():
    with patch("api.load_documents", side_effect = OSError("disk failure")):
        response = client.post("/search", json={"query" : "agent"})
    assert response.status_code == 500
    assert response.json() == {"detail": "failed to load documents"}

def test_ask_dependency_overrides():
    fake_store = object()
    fake_client = object()
    expected_answer = RAGAnswer(answer="offline answer", sources=[])

    app.dependency_overrides[get_vector_store] = lambda: fake_store
    app.dependency_overrides[get_llm_client] = lambda: fake_client
    try:
        with patch("api.answer_question", return_value=expected_answer) as mock_answer_question:
            response = client.post(
                "/ask",
                json={"query": "docker", "k": 2},
            )

        assert response.status_code == 200
        assert response.json() == {"answer": "offline answer", "sources": []}
        mock_answer_question.assert_called_once_with(
            query="docker",
            store=fake_store,
            client=fake_client,
            k=2,
        )
    finally:
        app.dependency_overrides.pop(get_vector_store, None)
        app.dependency_overrides.pop(get_llm_client, None)