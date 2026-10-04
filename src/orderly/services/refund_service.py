"""Business rules for refund records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.refund import Refund
from orderly.repositories.refund_repository import RefundRepository


class RefundService:
    """Coordinates refund reads and writes."""

    def __init__(self, repository: RefundRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Refund:
        """Validate and store a new refund."""
        self._validate(payload)
        return self.repository.add(Refund.from_dict(payload))

    def fetch(self, record_id: str) -> Refund:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no refund with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or charge_id."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("charge_id"):
            raise ValidationError("charge_id", "is required")
