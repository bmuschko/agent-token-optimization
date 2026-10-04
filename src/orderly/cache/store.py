"""A small thread-safe TTL cache."""
import threading
import time
from typing import Any, Dict, Optional, Tuple


class TTLCache:
    """A dictionary whose entries expire after a fixed number of seconds."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = ttl_seconds
        self._entries: Dict[str, Tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Return a live value, or None when missing or expired."""
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if expires_at < time.monotonic():
                del self._entries[key]
                return None
            return value

    def set(self, key: str, value: Any) -> None:
        """Store a value with a fresh expiry."""
        with self._lock:
            self._entries[key] = (time.monotonic() + self.ttl_seconds, value)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)

    def clear(self) -> None:
        """Drop every entry."""
        with self._lock:
            self._entries.clear()
