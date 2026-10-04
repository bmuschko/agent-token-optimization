"""A tiny HTTP transport seam so tests can substitute a fake."""
from typing import Any, Dict


class Transport:
    """The interface the integration clients depend on."""

    def get(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Issue a GET request."""
        raise NotImplementedError

    def post(self, url: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Issue a POST request."""
        raise NotImplementedError


class RecordingTransport(Transport):
    """A transport that replays scripted responses and records calls."""

    def __init__(self, responses=None) -> None:
        self.responses = list(responses or [])
        self.calls = []

    def _next(self, url, payload):
        self.calls.append((url, payload))
        if not self.responses:
            return {"ok": True}
        result = self.responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def get(self, url, params):
        return self._next(url, params)

    def post(self, url, body):
        return self._next(url, body)
