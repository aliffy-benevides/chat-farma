import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_ollama_embeddings(monkeypatch: pytest.MonkeyPatch):
    """Mock OllamaEmbeddings globally to prevent HTTP calls in unit tests.

    The fake implements the minimal interface used by LangChain vectorstores
    (FAISS.from_documents), i.e. embed_documents/embed_query.
    """

    import src.rag.rag as rag_module

    class FakeEmbeddings:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [[0.0, 0.0, 0.0] for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            return [0.0, 0.0, 0.0]

    monkeypatch.setattr(rag_module, "OllamaEmbeddings", FakeEmbeddings)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    """Default app client with external integrations stubbed.

    Important: stubs must be applied before app creation and before any indexing.
    """

    # Import inside fixture so monkeypatch is applied before app creation
    import src.main

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
    # IMPORTANT: mock indexing/retrieval build to avoid OllamaEmbeddings/FAISS touching Ollama.
    monkeypatch.setattr(
        src.main,
        "build_faiss_from_dir",
        lambda _: DummyRag([DummyDoc("conteudo", source="doc1")]),
    )

    class DummyLLM:
        def invoke(self, messages):
            return type("Resp", (), {"content": "resposta"})()

    # IMPORTANT: mock LLM factory to avoid any ChatOllama instantiation / HTTP calls.
    monkeypatch.setattr(src.main, "get_llm", lambda model: DummyLLM())
    monkeypatch.setattr(src.main, "answer_with_context", lambda llm, user_message, sources: "resposta")

    app = src.main.create_app()
    return TestClient(app)
