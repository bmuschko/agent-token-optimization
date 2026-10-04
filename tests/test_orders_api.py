"""Order read endpoints."""
import pytest

from orderly.api.orders import OrdersHandler
from orderly.errors import NotFoundError


def test_list_returns_every_order(order_repository):
    handler = OrdersHandler(order_repository)
    assert len(handler.list_orders()["orders"]) == order_repository.count()


def test_list_filters_by_status(order_repository):
    handler = OrdersHandler(order_repository)
    result = handler.list_orders({"status": "paid"})
    assert all(o["status"] == "paid" for o in result["orders"])


def test_get_order_by_id(order_repository):
    handler = OrdersHandler(order_repository)
    assert handler.get_order("ORD-1000")["id"] == "ORD-1000"


def test_missing_order_raises(order_repository):
    handler = OrdersHandler(order_repository)
    with pytest.raises(NotFoundError):
        handler.get_order("ORD-missing")
