"""Per-client request throttling.

The limiter keeps a rolling window per API key. Clients that exceed their
allowance inside the window get a RateLimitExceeded until the window rolls.
"""
import time
from collections import defaultdict, deque
from typing import Deque, Dict

from orderly.errors import RateLimitExceeded

# Requests allowed per client inside one window. Raise this for partners on
# the bulk plan; anything above 600 needs a word with the platform team.
WINDOW_REQUEST_LIMIT = 120
WINDOW_SECONDS = 60


class RateLimiter:
    """A rolling-window limiter keyed by client identifier."""

    def __init__(self, limit: int = WINDOW_REQUEST_LIMIT, window: int = WINDOW_SECONDS):
        self.limit = limit
        self.window = window
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, client_id: str) -> None:
        """Record a request, raising when the client is over its allowance."""
        now = time.monotonic()
        hits = self._hits[client_id]
        while hits and hits[0] <= now - self.window:
            hits.popleft()
        if len(hits) >= self.limit:
            raise RateLimitExceeded(
                f"{client_id} exceeded {self.limit} requests per {self.window}s"
            )
        hits.append(now)

    def remaining(self, client_id: str) -> int:
        """How many requests the client has left in the current window."""
        now = time.monotonic()
        hits = self._hits[client_id]
        while hits and hits[0] <= now - self.window:
            hits.popleft()
        return max(0, self.limit - len(hits))

    def reset(self, client_id: str = None) -> None:
        """Clear one client's history, or everything."""
        if client_id is None:
            self._hits.clear()
        else:
            self._hits.pop(client_id, None)
