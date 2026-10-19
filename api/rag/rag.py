from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class RagArtifacts:
    vectorstore: FAISS


def build_faiss_from_dir(reference_dir: str) -> RagArtifacts:
    """Builds a FAISS index from local reference files.

    MVP constraints:
    - Sources are curated by the team and live on disk.
    - This builds the index at runtime for simplicity.

    Supported file types here are kept minimal (txt/md).
    """

    ref_path = Path(reference_dir)
    if not ref_path.exists():
        raise FileNotFoundError(
            f"RAG_REFERENCE_DIR not found: {reference_dir}. "
            "Create it and add .txt/.md reference files."
        )

    loader = DirectoryLoader(
        str(ref_path),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        silent_errors=True,
    )
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(
        model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )

    # Ensure each chunk has a stable source id in metadata
    normalized: list[Document] = []
    for c in chunks:
        c.metadata = c.metadata or {}
        c.metadata.setdefault("source", c.metadata.get("source", "unknown"))
        normalized.append(c)

    vectorstore = FAISS.from_documents(normalized, embeddings)
    return RagArtifacts(vectorstore=vectorstore)
