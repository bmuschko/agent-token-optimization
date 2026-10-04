"""The refund model."""
from typing import Any, Dict


class Refund:
    """A refund record."""

    def __init__(self, id: str, charge_id: str = '', amount_cents: str = '', reason: str = '') -> None:
        self.id = id
        self.charge_id = charge_id
        self.amount_cents = amount_cents
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "charge_id": self.charge_id, "amount_cents": self.amount_cents, "reason": self.reason}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Refund":
        """Build a refund from a plain dictionary."""
        fields = ('charge_id', 'amount_cents', 'reason',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Refund {self.id}>"
