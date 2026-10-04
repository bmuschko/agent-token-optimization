"""The product model."""
from typing import Any, Dict


class Product:
    """A product record."""

    def __init__(self, id: str, sku: str = '', title: str = '', price_cents: str = '') -> None:
        self.id = id
        self.sku = sku
        self.title = title
        self.price_cents = price_cents

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dictionary."""
        return {"id": self.id, "sku": self.sku, "title": self.title, "price_cents": self.price_cents}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Build a product from a plain dictionary."""
        fields = ('sku', 'title', 'price_cents',)
        return cls(id=data["id"], **{k: data.get(k, "") for k in fields})

    def __repr__(self) -> str:
        return f"<Product {self.id}>"
