"""The address model."""
from typing import Any, Dict


class Address:
    """A address record."""

    def __init__(self, id: str, line1: str = '', city: str = '', postcode: str = '') -> None:
        self.id = id
        self.line1 = line1
        self.city = city
        self.postcode = postcode

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "line1": self.line1, "city": self.city, "postcode": self.postcode}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Address":
        """Build a address from a plain dictionary."""
        fields = ('line1', 'city', 'postcode',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Address {self.id}>"
