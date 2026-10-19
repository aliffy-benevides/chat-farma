from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class SourceSnippet(BaseModel):
    source_id: str
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceSnippet] = Field(default_factory=list)
    refused: bool = False
