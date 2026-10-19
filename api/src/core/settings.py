from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = Field(default="Chat Farma API")
    APP_VERSION: str = Field(default="0.1.0")

    ENVIRONMENT: str = Field(default="local")
    DEBUG: bool = Field(default=False)

    # LLM / RAG (Ollama local)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    OLLAMA_CHAT_MODEL: str = Field(default="llama3.1")
    OLLAMA_EMBEDDING_MODEL: str = Field(default="nomic-embed-text")

    RAG_REFERENCE_DIR: str = Field(default="data/references")
    RAG_TOP_K: int = Field(default=4)


@lru_cache
def get_settings() -> Settings:
    return Settings()
