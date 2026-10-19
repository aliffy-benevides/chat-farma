from __future__ import annotations

import os
from typing import Any

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


SYSTEM_PROMPT = """Você é o Chat Farma (MVP). Regras obrigatórias:

1) Responda SOMENTE usando as fontes fornecidas no contexto (trechos recuperados do acervo).
2) Se o contexto não contiver evidência suficiente, recuse: diga que não encontrou suporte nas referências do MVP e sugira termos para busca/reformulação.
3) Sempre inclua a seção 'Fontes usadas' com citações (identificadores) e, quando possível, trechos relevantes.
4) Se faltarem dados clínicos para concluir (idade, peso, ClCr, indicação etc.), faça perguntas objetivas antes de concluir.
5) Não faça recomendações prescritivas fora do que está nas fontes; diferencie informação geral de decisão clínica.
"""


def get_llm(model: str, temperature: float = 0.2) -> ChatOllama:
    # base_url is read from env by langchain-ollama, but we also pass it explicitly
    # to reduce surprises.

    return ChatOllama(
        model=model,
        temperature=temperature,
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )


def format_context_snippets(hits: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for i, h in enumerate(hits, start=1):
        src = h.get("source", "unknown")
        content = h.get("content", "")
        parts.append(f"[Fonte {i}] {src}\n{content}")
    return "\n\n".join(parts)


def answer_with_context(llm: ChatOllama, user_message: str, hits: list[dict[str, Any]]) -> str:
    context = format_context_snippets(hits)

    prompt = f"""Pergunta do usuário:
{user_message}

Contexto (fontes recuperadas):
{context}

Instruções de resposta:
- Se o contexto não responder, recuse conforme regra 2.
- Estruture a resposta em:
  1) Resposta
  2) Limitações / dados faltantes (se aplicável)
  3) Fontes usadas (lista com os identificadores acima)
"""

    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]
    resp = llm.invoke(messages)
    return resp.content
