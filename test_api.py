from fastapi.testclient import TestClient
from api import app
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