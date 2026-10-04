"""The webhook model."""
from typing import Any, Dict


class Webhook:
    """A webhook record."""

    def __init__(self, id: str, url: str = '', event: str = '', secret: str = '') -> None:
        self.id = id
        self.url = url
        self.event = event
        self.secret = secret

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "url": self.url, "event": self.event, "secret": self.secret}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Webhook":
        """Build a webhook from a plain dictionary."""
        fields = ('url', 'event', 'secret',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Webhook {self.id}>"
