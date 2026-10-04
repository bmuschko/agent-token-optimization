"""The customer model."""
from typing import Any, Dict


class Customer:
    """A customer record."""

    def __init__(self, id: str, email: str = '', name: str = '', tier: str = '') -> None:
        self.id = id
        self.email = email
        self.name = name
        self.tier = tier

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "email": self.email, "name": self.name, "tier": self.tier}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        """Build a customer from a plain dictionary."""
        fields = ('email', 'name', 'tier',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Customer {self.id}>"
