"""Runtime configuration, read once at import time."""
import os
from dataclasses import dataclass


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Everything the service reads from the environment."""

    database_url: str = os.environ.get("ORDERLY_DATABASE_URL", "sqlite:///orderly.db")
    cache_ttl_seconds: int = _int_env("ORDERLY_CACHE_TTL", 300)
    cache_warm_workers: int = _int_env("ORDERLY_CACHE_WORKERS", 8)
    request_timeout_seconds: int = _int_env("ORDERLY_TIMEOUT", 10)
    retry_attempts: int = _int_env("ORDERLY_RETRY_ATTEMPTS", 3)
    default_page_size: int = _int_env("ORDERLY_PAGE_SIZE", 25)
    max_page_size: int = _int_env("ORDERLY_MAX_PAGE_SIZE", 200)
    default_currency: str = os.environ.get("ORDERLY_CURRENCY", "USD")


settings = Settings()
