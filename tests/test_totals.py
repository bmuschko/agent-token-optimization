"""Order total assembly."""
import pytest

from orderly.pricing.totals import line_subtotal, order_subtotal, order_total

LINES = [
    {"sku": "A", "quantity": 2, "unit_price_cents": 1000},
    {"sku": "B", "quantity": 1, "unit_price_cents": 500},
]


def test_line_subtotal():
    assert line_subtotal(1000, 3) == 3000


def test_negative_quantity_is_rejected():
    with pytest.raises(ValueError):
        line_subtotal(1000, -1)


def test_order_subtotal_sums_lines():
    assert order_subtotal(LINES) == 2500


def test_order_total_breakdown_is_consistent():
    result = order_total(LINES)
    taxable = result["subtotal_cents"] - result["discount_cents"]
    assert result["total_cents"] == taxable + result["tax_cents"]
