from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

import src.rag.agent as agent


@dataclass
class DummyResponse:
    content: str


class DummyLLM:
    def __init__(self) -> None:
        self.invocations: list[list[Any]] = []

    def invoke(self, messages: list[Any]) -> DummyResponse:
        self.invocations.append(messages)
        return DummyResponse(content="ok")


def test_format_context_snippets_formats_and_defaults_unknown() -> None:
    sources = [
        agent.SourceSnippet(source_id="doc1.txt", snippet="trecho 1"),
        agent.SourceSnippet(source_id="unknown", snippet="trecho 2 sem source"),
        agent.SourceSnippet(source_id="unknown", snippet=""),
    ]

    out = agent.format_context_snippets(sources)

    assert "[Fonte 1] doc1.txt\ntrecho 1" in out
    assert "[Fonte 2] unknown\ntrecho 2 sem source" in out
    assert "[Fonte 3] unknown\n" in out
    assert "\n\n" in out  # separator between snippets


def test_answer_with_context_calls_llm_and_returns_content() -> None:
    llm = DummyLLM()

    sources = [agent.SourceSnippet(source_id="doc1", snippet="conteudo")]
    out = agent.answer_with_context(llm=llm, user_message="pergunta?", sources=sources)

    assert out == "ok"
    assert len(llm.invocations) == 1

    messages = llm.invocations[0]
    assert len(messages) == 2

    # The system message must include the policy prompt
    assert agent.SYSTEM_PROMPT.strip().splitlines()[0] in messages[0].content

    # The human message must include user question and formatted context
    human = messages[1].content
    assert "Pergunta do usuário:" in human
    assert "pergunta?" in human
    assert "Contexto (fontes recuperadas):" in human
    assert "[Fonte 1] doc1" in human
    assert "conteudo" in human


def test_get_llm_uses_default_base_url_when_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    # We don't want to instantiate the real ChatOllama in unit tests.
    created: dict[str, Any] = {}

    class FakeChat:
        def __init__(self, **kwargs: Any) -> None:
            created.update(kwargs)

    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.setattr(agent, "ChatOllama", FakeChat)

    llm = agent.get_llm(model="m", temperature=0.7)

    assert isinstance(llm, FakeChat)
    assert created["model"] == "m"
    assert created["temperature"] == 0.7
    assert created["base_url"] == "http://localhost:11434"


def test_get_llm_uses_env_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    created: dict[str, Any] = {}

    class FakeChat:
        def __init__(self, **kwargs: Any) -> None:
            created.update(kwargs)

    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama:11434")
    monkeypatch.setattr(agent, "ChatOllama", FakeChat)

    _ = agent.get_llm(model="m")

    assert created["base_url"] == "http://ollama:11434"
