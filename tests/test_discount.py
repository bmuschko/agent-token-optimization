"""Volume discount behaviour away from the tier boundaries."""
from orderly.pricing.discount import (
    describe_tier,
    discount_cents,
    rate_for_subtotal,
    total_after_discount,
)


def test_small_order_gets_no_discount():
    assert rate_for_subtotal(5_00) == 0.0


def test_mid_tier_order_gets_five_percent():
    assert rate_for_subtotal(250_00) == 0.05


def test_large_order_gets_ten_percent():
    assert rate_for_subtotal(750_00) == 0.10


def test_discount_is_applied_to_total():
    assert total_after_discount(250_00) == 250_00 - discount_cents(250_00)


def test_negative_subtotal_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        rate_for_subtotal(-1)


def test_describe_tier_reads_back():
    assert describe_tier(5_00) == "no volume discount"
    assert describe_tier(250_00) == "5% volume discount"
