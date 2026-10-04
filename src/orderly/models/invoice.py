"""The invoice model."""
from typing import Any, Dict


class Invoice:
    """A invoice record."""

    def __init__(self, id: str, order_id: str = '', issued_at: str = '', total_cents: str = '') -> None:
        self.id = id
        self.order_id = order_id
        self.issued_at = issued_at
        self.total_cents = total_cents

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "order_id": self.order_id, "issued_at": self.issued_at, "total_cents": self.total_cents}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Invoice":
        """Build a invoice from a plain dictionary."""
        fields = ('order_id', 'issued_at', 'total_cents',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Invoice {self.id}>"
