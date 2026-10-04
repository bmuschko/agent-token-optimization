"""Persistence for address records."""
from typing import Dict, List, Optional

from orderly.models.address import Address


class AddressRepository:
    """Stores address records in memory."""

    def __init__(self, records: Optional[List[Address]] = None) -> None:
        self._records: Dict[str, Address] = {r.id: r for r in (records or [])}

    def all(self) -> List[Address]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Address]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Address) -> Address:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_line1(self, value: str) -> List[Address]:
        """Every record whose line1 matches."""
        return [r for r in self._records.values() if getattr(r, "line1") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
