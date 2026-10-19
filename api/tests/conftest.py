import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    """Default app client with external integrations stubbed.

    Tests that need different behavior can still monkeypatch before importing main.
    """

    # Import inside fixture so monkeypatch is applied before app creation
    import main

    class DummyDoc:
        def __init__(self, content: str, source: str = "src") -> None:
            self.page_content = content
            self.metadata = {"source": source}

    class DummyRetriever:
        def __init__(self, docs):
            self._docs = docs

        def invoke(self, message: str):
            return self._docs

    class DummyVectorStore:
        def __init__(self, docs):
            self._docs = docs

        def as_retriever(self, search_kwargs=None):
            return DummyRetriever(self._docs)

    class DummyRag:
        def __init__(self, docs):
            self.vectorstore = DummyVectorStore(docs)

    # Default stub: 1 doc so /chat has context by default
    monkeypatch.setattr(
        main,
        "build_faiss_from_dir",
        lambda _: DummyRag([DummyDoc("conteudo", source="doc1")]),
    )

    class DummyLLM:
        def invoke(self, messages):
            return type("Resp", (), {"content": "resposta"})()

    monkeypatch.setattr(main, "get_llm", lambda model: DummyLLM())
    monkeypatch.setattr(main, "answer_with_context", lambda llm, user_message, hits: "resposta")

    app = main.create_app()
    return TestClient(app)
