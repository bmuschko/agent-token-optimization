"""Business rules for invoice records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.invoice import Invoice
from orderly.repositories.invoice_repository import InvoiceRepository


class InvoiceService:
    """Coordinates invoice reads and writes."""

    def __init__(self, repository: InvoiceRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Invoice:
        """Validate and store a new invoice."""
        self._validate(payload)
        return self.repository.add(Invoice.from_dict(payload))

    def fetch(self, record_id: str) -> Invoice:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no invoice with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or order_id."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("order_id"):
            raise ValidationError("order_id", "is required")
