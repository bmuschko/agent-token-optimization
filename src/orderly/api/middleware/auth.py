"""API key authentication."""
from typing import Dict, Optional


class ApiKeyAuth:
    """Resolves an API key to a client identifier."""

    def __init__(self, keys: Dict[str, str]) -> None:
        self.keys = keys

    def client_for(self, api_key: Optional[str]) -> Optional[str]:
        """Return the client id for a key, or None when the key is unknown."""
        if not api_key:
            return None
        return self.keys.get(api_key)

    def is_valid(self, api_key: Optional[str]) -> bool:
        """Whether a key resolves to a known client."""
        return self.client_for(api_key) is not None
