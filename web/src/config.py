from __future__ import annotations

import os


def get_api_url() -> str:
    return os.getenv("CHATFARMA_API_URL", "http://api:8000").rstrip("/")


def get_http_timeout() -> int:
    try:
        return int(os.getenv("CHATFARMA_HTTP_TIMEOUT", "60"))
    except ValueError:
        return 60
