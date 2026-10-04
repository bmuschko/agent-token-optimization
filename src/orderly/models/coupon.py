"""The coupon model."""
from typing import Any, Dict


class Coupon:
    """A coupon record."""

    def __init__(self, id: str, code: str = '', percent_off: str = '', expires_at: str = '') -> None:
        self.id = id
        self.code = code
        self.percent_off = percent_off
        self.expires_at = expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "code": self.code, "percent_off": self.percent_off, "expires_at": self.expires_at}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Coupon":
        """Build a coupon from a plain dictionary."""
        fields = ('code', 'percent_off', 'expires_at',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Coupon {self.id}>"
