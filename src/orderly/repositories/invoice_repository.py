"""Persistence for invoice records."""
from typing import Dict, List, Optional

from orderly.models.invoice import Invoice


class InvoiceRepository:
    """Stores invoice records in memory."""

    def __init__(self, records: Optional[List[Invoice]] = None) -> None:
        self._records: Dict[str, Invoice] = {r.id: r for r in (records or [])}

    def all(self) -> List[Invoice]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Invoice]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Invoice) -> Invoice:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_order_id(self, value: str) -> List[Invoice]:
        """Every record whose order_id matches."""
        return [r for r in self._records.values() if getattr(r, "order_id") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
