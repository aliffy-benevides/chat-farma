from __future__ import annotations

from typing import Any

import requests
from pydantic import BaseModel

from .config import get_api_url, get_http_timeout


class SourceSnippet(BaseModel):
    source_id: str
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceSnippet] = []
    refused: bool = False


def health() -> dict[str, Any]:
    base = get_api_url()
    timeout = get_http_timeout()
    r = requests.get(f"{base}/health", timeout=timeout)
    r.raise_for_status()
    return r.json()


def chat(message: str) -> ChatResponse:
    base = get_api_url()
    timeout = get_http_timeout()
    r = requests.post(f"{base}/chat", json={"message": message}, timeout=timeout)
    r.raise_for_status()
    return ChatResponse.model_validate(r.json())
