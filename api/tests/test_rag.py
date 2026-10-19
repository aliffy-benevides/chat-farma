from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

import src.rag.rag as rag_module


@dataclass
class DummyVectorStore:
    docs: list[Any]
    embeddings: Any


def test_build_faiss_from_dir_raises_when_dir_missing(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"

    with pytest.raises(FileNotFoundError) as exc:
        rag_module.build_faiss_from_dir(str(missing))

    assert "RAG_REFERENCE_DIR not found" in str(exc.value)


def test_build_faiss_from_dir_builds_index_and_normalizes_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange: create reference directory and a txt file (not actually read because we stub loader)
    ref_dir = tmp_path / "refs"
    ref_dir.mkdir()
    (ref_dir / "a.txt").write_text("conteudo", encoding="utf-8")

    # Fake loader returns docs
    class FakeDirectoryLoader:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.args = args
            self.kwargs = kwargs

        def load(self) -> list[Any]:
            return ["DOC1", "DOC2"]

    # Fake splitter returns chunks with varying metadata
    class FakeSplitter:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def split_documents(self, docs: list[Any]) -> list[Any]:
            class Chunk:
                def __init__(self, page_content: str, metadata: dict[str, Any] | None):
                    self.page_content = page_content
                    self.metadata = metadata

            return [
                Chunk("c1", None),
                Chunk("c2", {}),
                Chunk("c3", {"source": "s3"}),
            ]

    # OllamaEmbeddings is mocked globally in tests/conftest.py,
    # but for this test we want to assert which kwargs were used.
    created_embeddings: dict[str, Any] = {}

    class FakeEmbeddings:
        def __init__(self, **kwargs: Any) -> None:
            created_embeddings.update(kwargs)

    monkeypatch.setattr(rag_module, "OllamaEmbeddings", FakeEmbeddings)

    captured: dict[str, Any] = {}

    class FakeFAISS:
        @staticmethod
        def from_documents(docs: list[Any], embeddings: Any) -> DummyVectorStore:
            captured["docs"] = docs
            captured["embeddings"] = embeddings
            return DummyVectorStore(docs=docs, embeddings=embeddings)

    monkeypatch.setenv("OLLAMA_EMBEDDING_MODEL", "embed-model")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama:11434")

    monkeypatch.setattr(rag_module, "DirectoryLoader", FakeDirectoryLoader)
    monkeypatch.setattr(rag_module, "RecursiveCharacterTextSplitter", FakeSplitter)
    # OllamaEmbeddings is mocked globally in tests/conftest.py
    monkeypatch.setattr(rag_module, "FAISS", FakeFAISS)

    # Act
    artifacts = rag_module.build_faiss_from_dir(str(ref_dir))

    # Assert: embeddings constructed from env
    assert created_embeddings["model"] == "embed-model"
    assert created_embeddings["base_url"] == "http://ollama:11434"

    # Assert: FAISS called with normalized docs
    docs = captured["docs"]
    assert len(docs) == 3
    assert docs[0].metadata == {"source": "unknown"}
    assert docs[1].metadata == {"source": "unknown"}
    assert docs[2].metadata == {"source": "s3"}

    assert isinstance(artifacts.vectorstore, DummyVectorStore)


def test_build_faiss_from_dir_passes_expected_loader_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ref_dir = tmp_path / "refs"
    ref_dir.mkdir()

    init_args: dict[str, Any] = {}

    class FakeDirectoryLoader:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            init_args["args"] = args
            init_args["kwargs"] = kwargs

        def load(self) -> list[Any]:
            return []

    class FakeSplitter:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def split_documents(self, docs: list[Any]) -> list[Any]:
            return []

    class FakeEmbeddings:
        def __init__(self, **kwargs: Any) -> None:
            pass

    class FakeFAISS:
        @staticmethod
        def from_documents(docs: list[Any], embeddings: Any) -> DummyVectorStore:
            return DummyVectorStore(docs=docs, embeddings=embeddings)

    monkeypatch.setattr(rag_module, "DirectoryLoader", FakeDirectoryLoader)
    monkeypatch.setattr(rag_module, "RecursiveCharacterTextSplitter", FakeSplitter)
    # OllamaEmbeddings is mocked globally in tests/conftest.py
    monkeypatch.setattr(rag_module, "FAISS", FakeFAISS)

    _ = rag_module.build_faiss_from_dir(str(ref_dir))

    # Validate loader is configured as expected
    assert init_args["args"][0] == str(ref_dir)
    assert init_args["kwargs"]["glob"] == "**/*.txt"
    assert init_args["kwargs"]["loader_cls"] is rag_module.TextLoader
    assert init_args["kwargs"]["loader_kwargs"] == {"encoding": "utf-8"}
    assert init_args["kwargs"]["silent_errors"] is True
