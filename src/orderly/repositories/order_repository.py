"""Order persistence."""
from typing import Any, Dict, List, Optional


class OrderRepository:
    """Reads and writes orders held in memory."""

    def __init__(self, orders: Optional[List[Dict[str, Any]]] = None) -> None:
        self._orders = {o["id"]: o for o in (orders or [])}

    def all(self) -> List[Dict[str, Any]]:
        """Every order, in insertion order."""
        return list(self._orders.values())

    def get(self, order_id: str) -> Optional[Dict[str, Any]]:
        """One order by id, or None."""
        return self._orders.get(order_id)

    def add(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Insert or replace an order."""
        self._orders[order["id"]] = order
        return order

    def remove(self, order_id: str) -> bool:
        """Delete an order, reporting whether it existed."""
        return self._orders.pop(order_id, None) is not None

    def count(self) -> int:
        """How many orders are stored."""
        return len(self._orders)

    def by_status(self, status: str) -> List[Dict[str, Any]]:
        """Every order in a given status."""
        return [o for o in self._orders.values() if o["status"] == status]
