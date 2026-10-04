"""Order endpoints. Reference solution for T5."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError
from orderly.repositories.order_repository import OrderRepository
from orderly.utils.pagination import clamp_limit, clamp_offset, page


class OrdersHandler:
    """Read endpoints for orders."""

    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def list_orders(self, query: Dict[str, Any] = None) -> Dict[str, Any]:
        """Return a page of orders, optionally filtered.

        Query keys understood: customer_id, status, limit, offset.
        """
        query = query or {}
        orders = self.repository.all()
        if query.get("customer_id"):
            orders = [o for o in orders if o["customer_id"] == query["customer_id"]]
        if query.get("status"):
            orders = [o for o in orders if o["status"] == query["status"]]

        limit = clamp_limit(query.get("limit"))
        offset = clamp_offset(query.get("offset"))
        window = page(orders, limit, offset)
        return {
            "orders": window["items"],
            "total": window["total"],
            "limit": window["limit"],
            "offset": window["offset"],
            "has_more": window["has_more"],
        }

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Return a single order by id."""
        order = self.repository.get(order_id)
        if order is None:
            raise NotFoundError(f"no order with id {order_id}")
        return order

    def order_lines(self, order_id: str) -> List[Dict[str, Any]]:
        """Return the line items on an order."""
        return self.get_order(order_id)["lines"]
