"""Persistence for refund records."""
from typing import Dict, List, Optional

from orderly.models.refund import Refund


class RefundRepository:
    """Stores refund records in memory."""

    def __init__(self, records: Optional[List[Refund]] = None) -> None:
        self._records: Dict[str, Refund] = {r.id: r for r in (records or [])}

    def all(self) -> List[Refund]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Refund]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Refund) -> Refund:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_charge_id(self, value: str) -> List[Refund]:
        """Every record whose charge_id matches."""
        return [r for r in self._records.values() if getattr(r, "charge_id") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
