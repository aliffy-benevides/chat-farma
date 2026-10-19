from __future__ import annotations

from fastapi import FastAPI

from src.core.settings import get_settings
from src.rag.agent import answer_with_context, get_llm
from src.rag.rag import build_faiss_from_dir
from src.schemas import ChatRequest, ChatResponse, SourceSnippet


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )

    # Build a simple in-memory FAISS index at startup (MVP simplicity)
    rag = build_faiss_from_dir(settings.RAG_REFERENCE_DIR)
    retriever = rag.vectorstore.as_retriever(search_kwargs={"k": settings.RAG_TOP_K})

    llm = get_llm(model=settings.OLLAMA_CHAT_MODEL)

    @app.get("/health", tags=["health"])
    def health_check() -> dict:
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.post("/chat", response_model=ChatResponse, tags=["chat"])
    def chat(payload: ChatRequest) -> ChatResponse:
        docs = retriever.invoke(payload.message)

        hits = []
        sources: list[SourceSnippet] = []
        for d in docs:
            source_id = d.metadata.get("source", "unknown")
            snippet = (d.page_content or "")[:600]
            hits.append({"source": source_id, "content": snippet})
            sources.append(SourceSnippet(source_id=source_id, snippet=snippet))

        answer = answer_with_context(llm=llm, user_message=payload.message, hits=hits)

        # Simple refusal heuristic: agent instructed to refuse when no context.
        refused = len(docs) == 0

        return ChatResponse(answer=answer, sources=sources, refused=refused)

    return app


app = create_app()
