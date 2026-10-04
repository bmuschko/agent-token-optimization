"""Offset pagination helpers shared by the handlers."""
from typing import Any, Dict, List

from orderly.config import settings


def clamp_limit(limit: Any) -> int:
    """Coerce a requested page size into the allowed range."""
    try:
        value = int(limit)
    except (TypeError, ValueError):
        return settings.default_page_size
    if value <= 0:
        return settings.default_page_size
    return min(value, settings.max_page_size)


def clamp_offset(offset: Any) -> int:
    """Coerce a requested offset into a non-negative integer."""
    try:
        value = int(offset)
    except (TypeError, ValueError):
        return 0
    return max(0, value)


def page(items: List[Any], limit: int, offset: int) -> Dict[str, Any]:
    """Slice a list and describe the slice."""
    window = items[offset: offset + limit]
    return {
        "items": window,
        "total": len(items),
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(window) < len(items),
    }
