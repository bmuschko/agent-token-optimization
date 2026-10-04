"""Persistence for webhook records."""
from typing import Dict, List, Optional

from orderly.models.webhook import Webhook


class WebhookRepository:
    """Stores webhook records in memory."""

    def __init__(self, records: Optional[List[Webhook]] = None) -> None:
        self._records: Dict[str, Webhook] = {r.id: r for r in (records or [])}

    def all(self) -> List[Webhook]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Webhook]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Webhook) -> Webhook:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_url(self, value: str) -> List[Webhook]:
        """Every record whose url matches."""
        return [r for r in self._records.values() if getattr(r, "url") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
