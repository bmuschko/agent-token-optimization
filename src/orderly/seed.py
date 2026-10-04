"""Deterministic seed data so every exercise starts from the same place."""
from typing import Any, Dict, List

STATUSES = ("pending", "paid", "shipped", "cancelled")


def load_seed_orders(count: int = 24) -> List[Dict[str, Any]]:
    """Build a stable set of orders. Same input, same output, every run."""
    orders = []
    for index in range(count):
        line_count = (index % 3) + 1
        orders.append(
            {
                "id": f"ORD-{1000 + index}",
                "customer_id": f"CUST-{100 + (index % 7)}",
                "status": STATUSES[index % len(STATUSES)],
                "currency": "USD",
                "lines": [
                    {
                        "sku": f"SKU-{(index * 3 + n) % 40:03d}",
                        "quantity": (n % 4) + 1,
                        "unit_price_cents": 1250 + (index * 37 + n * 11) % 8000,
                    }
                    for n in range(line_count)
                ],
            }
        )
    return orders
