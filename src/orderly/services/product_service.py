"""Business rules for product records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.product import Product
from orderly.repositories.product_repository import ProductRepository


class ProductService:
    """Coordinates product reads and writes."""

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Product:
        """Validate and store a new product."""
        self._validate(payload)
        return self.repository.add(Product.from_dict(payload))

    def fetch(self, record_id: str) -> Product:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no product with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or sku."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("sku"):
            raise ValidationError("sku", "is required")
