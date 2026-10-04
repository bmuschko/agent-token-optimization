"""Persistence for shipment records."""
from typing import Dict, List, Optional

from orderly.models.shipment import Shipment


class ShipmentRepository:
    """Stores shipment records in memory."""

    def __init__(self, records: Optional[List[Shipment]] = None) -> None:
        self._records: Dict[str, Shipment] = {r.id: r for r in (records or [])}

    def all(self) -> List[Shipment]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Shipment]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Shipment) -> Shipment:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_order_id(self, value: str) -> List[Shipment]:
        """Every record whose order_id matches."""
        return [r for r in self._records.values() if getattr(r, "order_id") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
