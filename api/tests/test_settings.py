from __future__ import annotations

import importlib

import pytest


def _reload_settings_module():
    """Reload settings module to avoid lru_cache cross-test interference."""
    import core.settings as settings_module

    settings_module.get_settings.cache_clear()
    return importlib.reload(settings_module)


def test_get_settings_reads_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "Minha API")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://example:11434")
    monkeypatch.setenv("OLLAMA_CHAT_MODEL", "llamaX")
    monkeypatch.setenv("OLLAMA_EMBEDDING_MODEL", "embedX")
    monkeypatch.setenv("RAG_REFERENCE_DIR", "data/custom")
    monkeypatch.setenv("RAG_TOP_K", "7")

    settings_module = _reload_settings_module()

    s = settings_module.get_settings()

    assert s.APP_NAME == "Minha API"
    assert s.APP_VERSION == "9.9.9"
    assert s.ENVIRONMENT == "test"
    assert s.DEBUG is True
    assert s.OLLAMA_BASE_URL == "http://example:11434"
    assert s.OLLAMA_CHAT_MODEL == "llamaX"
    assert s.OLLAMA_EMBEDDING_MODEL == "embedX"
    assert s.RAG_REFERENCE_DIR == "data/custom"
    assert s.RAG_TOP_K == 7


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    # First call creates instance
    settings_module = _reload_settings_module()

    s1 = settings_module.get_settings()

    # Change env after first call; cached value should not change
    monkeypatch.setenv("APP_NAME", "Outro Nome")

    s2 = settings_module.get_settings()

    assert s1 is s2
    assert s2.APP_NAME == "Chat Farma API"


def test_cache_clear_allows_reloading_env(monkeypatch: pytest.MonkeyPatch) -> None:
    settings_module = _reload_settings_module()

    s1 = settings_module.get_settings()
    assert s1.APP_NAME == "Chat Farma API"

    monkeypatch.setenv("APP_NAME", "Nome Atualizado")

    settings_module.get_settings.cache_clear()
    s2 = settings_module.get_settings()

    assert s2.APP_NAME == "Nome Atualizado"
    assert s1 is not s2
