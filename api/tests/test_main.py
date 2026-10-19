from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient


def test_health_success(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200

    data = resp.json()
    assert data["status"] == "ok"
    assert "app" in data
    assert "version" in data
    assert "environment" in data


def test_chat_success_returns_answer_and_sources(client: TestClient) -> None:
    resp = client.post("/chat", json={"message": "qualquer"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["answer"] == "resposta"
    assert data["refused"] is False
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) == 1
    assert data["sources"][0]["source_id"] == "doc1"
    assert data["sources"][0]["snippet"] == "conteudo"


def test_chat_refused_when_no_docs(monkeypatch: pytest.MonkeyPatch) -> None:
    # Build a client where retriever returns no docs
    import src.main

    class DummyRetriever:
        def invoke(self, message: str):
            return []

    class DummyVectorStore:
        def as_retriever(self, search_kwargs=None):
            return DummyRetriever()

    class DummyRag:
        vectorstore = DummyVectorStore()

    monkeypatch.setattr(src.main, "build_faiss_from_dir", lambda _: DummyRag())
    monkeypatch.setattr(src.main, "get_llm", lambda model: object())

    # Even with no docs, answer_with_context will be called; keep it deterministic
    monkeypatch.setattr(src.main, "answer_with_context", lambda llm, user_message, hits: "sem contexto")

    c = TestClient(src.main.create_app())

    resp = c.post("/chat", json={"message": "x"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["answer"] == "sem contexto"
    assert data["sources"] == []
    assert data["refused"] is True


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"message": ""},
        {"message": "a" * 8001},
        {"message": None},
    ],
)
def test_chat_validation_errors(payload: dict[str, Any], client: TestClient) -> None:
    resp = client.post("/chat", json=payload)
    assert resp.status_code == 422
