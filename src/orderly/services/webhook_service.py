"""Business rules for webhook records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.webhook import Webhook
from orderly.repositories.webhook_repository import WebhookRepository


class WebhookService:
    """Coordinates webhook reads and writes."""

    def __init__(self, repository: WebhookRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Webhook:
        """Validate and store a new webhook."""
        self._validate(payload)
        return self.repository.add(Webhook.from_dict(payload))

    def fetch(self, record_id: str) -> Webhook:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no webhook with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or url."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("url"):
            raise ValidationError("url", "is required")
