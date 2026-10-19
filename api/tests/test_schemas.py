from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.schemas import ChatRequest, ChatResponse, SourceSnippet


def test_chat_request_accepts_valid_message() -> None:
    req = ChatRequest(message="oi")
    assert req.message == "oi"


def test_chat_request_rejects_empty_message() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="")


def test_chat_request_rejects_message_over_max_length() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="a" * 8001)


def test_source_snippet_requires_fields() -> None:
    snip = SourceSnippet(source_id="doc1", snippet="trecho")
    assert snip.source_id == "doc1"
    assert snip.snippet == "trecho"

    with pytest.raises(ValidationError):
        SourceSnippet(source_id="doc1")  # type: ignore[call-arg]


def test_chat_response_defaults() -> None:
    resp = ChatResponse(answer="ok")
    assert resp.answer == "ok"
    assert resp.sources == []
    assert resp.refused is False


def test_chat_response_accepts_sources_and_refused() -> None:
    resp = ChatResponse(
        answer="a",
        refused=True,
        sources=[SourceSnippet(source_id="s", snippet="t")],
    )
    assert resp.refused is True
    assert len(resp.sources) == 1
    assert resp.sources[0].source_id == "s"
