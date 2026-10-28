"""Currency conversion."""
from decimal import Decimal

from orderly.pricing.currency import from_minor, minor_units, to_minor


def test_two_decimal_currency():
    assert minor_units("USD") == 2


def test_to_minor_rounds_half_up():
    assert to_minor(Decimal("10.005"), "USD") == 1001


def test_round_trips():
    assert from_minor(1234, "USD") == Decimal("12.34")
