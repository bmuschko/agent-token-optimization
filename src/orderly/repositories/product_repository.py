"""Persistence for product records."""
from typing import Dict, List, Optional

from orderly.models.product import Product


class ProductRepository:
    """Stores product records in memory."""

    def __init__(self, records: Optional[List[Product]] = None) -> None:
        self._records: Dict[str, Product] = {r.id: r for r in (records or [])}

    def all(self) -> List[Product]:
        """Every stored record."""
        return list(self._records.values())

    def get(self, record_id: str) -> Optional[Product]:
        """One record by id, or None."""
        return self._records.get(record_id)

    def add(self, record: Product) -> Product:
        """Insert or replace a record."""
        self._records[record.id] = record
        return record

    def remove(self, record_id: str) -> bool:
        """Delete a record, reporting whether it existed."""
        return self._records.pop(record_id, None) is not None

    def find_by_sku(self, value: str) -> List[Product]:
        """Every record whose sku matches."""
        return [r for r in self._records.values() if getattr(r, "sku") == value]

    def count(self) -> int:
        """How many records are stored."""
        return len(self._records)
