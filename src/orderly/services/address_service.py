"""Business rules for address records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.address import Address
from orderly.repositories.address_repository import AddressRepository


class AddressService:
    """Coordinates address reads and writes."""

    def __init__(self, repository: AddressRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Address:
        """Validate and store a new address."""
        self._validate(payload)
        return self.repository.add(Address.from_dict(payload))

    def fetch(self, record_id: str) -> Address:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no address with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or line1."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("line1"):
            raise ValidationError("line1", "is required")
