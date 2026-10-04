"""Identifier helpers."""
import hashlib
import uuid


def new_id(prefix: str) -> str:
    """A fresh prefixed identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def stable_id(prefix: str, *parts: str) -> str:
    """A deterministic identifier derived from its parts."""
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return f"{prefix}-{digest[:12]}"


def is_prefixed(value: str, prefix: str) -> bool:
    """Whether an identifier carries the expected prefix."""
    return value.startswith(prefix + "-")
