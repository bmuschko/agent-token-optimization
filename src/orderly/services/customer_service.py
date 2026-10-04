"""Business rules for customer records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.customer import Customer
from orderly.repositories.customer_repository import CustomerRepository


class CustomerService:
    """Coordinates customer reads and writes."""

    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Customer:
        """Validate and store a new customer."""
        self._validate(payload)
        return self.repository.add(Customer.from_dict(payload))

    def fetch(self, record_id: str) -> Customer:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no customer with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or email."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("email"):
            raise ValidationError("email", "is required")
