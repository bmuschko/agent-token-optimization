"""T5 acceptance: list_orders paginates."""
from orderly.api.orders import OrdersHandler


def test_limit_caps_the_page(order_repository):
    result = OrdersHandler(order_repository).list_orders({"limit": 5})
    assert len(result["orders"]) == 5


def test_offset_moves_the_window(order_repository):
    handler = OrdersHandler(order_repository)
    first = handler.list_orders({"limit": 5, "offset": 0})["orders"]
    second = handler.list_orders({"limit": 5, "offset": 5})["orders"]
    assert first[0]["id"] != second[0]["id"]


def test_response_reports_the_total(order_repository):
    result = OrdersHandler(order_repository).list_orders({"limit": 5})
    assert result["total"] == order_repository.count()
    assert result["has_more"] is True


def test_filters_still_apply(order_repository):
    result = OrdersHandler(order_repository).list_orders({"status": "paid", "limit": 2})
    assert all(o["status"] == "paid" for o in result["orders"])


def test_no_query_still_works(order_repository):
    assert OrdersHandler(order_repository).list_orders()["orders"]
