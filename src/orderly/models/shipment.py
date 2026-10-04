"""The shipment model."""
from typing import Any, Dict


class Shipment:
    """A shipment record."""

    def __init__(self, id: str, order_id: str = '', carrier: str = '', tracking: str = '') -> None:
        self.id = id
        self.order_id = order_id
        self.carrier = carrier
        self.tracking = tracking

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "order_id": self.order_id, "carrier": self.carrier, "tracking": self.tracking}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Shipment":
        """Build a shipment from a plain dictionary."""
        fields = ('order_id', 'carrier', 'tracking',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Shipment {self.id}>"
