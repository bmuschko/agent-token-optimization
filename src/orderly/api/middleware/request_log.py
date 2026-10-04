"""Structured request logging."""
import json
import sys
import time


class RequestLog:
    """Writes one JSON line per request."""

    def __init__(self, stream=None) -> None:
        self.stream = stream or sys.stdout

    def record(self, method: str, path: str, status: int, started_at: float) -> None:
        """Emit a single structured log line."""
        entry = {
            "method": method,
            "path": path,
            "status": status,
            "duration_ms": round((time.monotonic() - started_at) * 1000, 2),
        }
        self.stream.write(json.dumps(entry) + "\n")
