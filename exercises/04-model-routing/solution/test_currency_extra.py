"""Reference solution for T7: the branches tests/test_currency.py misses."""
from decimal import Decimal

import pytest

from orderly.errors import UnsupportedCurrencyError
from orderly.pricing.currency import (
    format_amount,
    from_minor,
    minor_units,
    split_evenly,
    to_minor,
    truncate_to_minor,
)


def test_zero_decimal_currency_has_no_minor_units():
    assert minor_units("JPY") == 0


def test_three_decimal_currency():
    assert minor_units("BHD") == 3


def test_currency_code_is_case_insensitive():
    assert minor_units("usd") == 2


def test_unknown_currency_raises():
    with pytest.raises(UnsupportedCurrencyError):
        minor_units("XYZ")


def test_to_minor_for_zero_decimal_currency():
    assert to_minor(Decimal("1250"), "JPY") == 1250


def test_to_minor_for_three_decimal_currency():
    assert to_minor(Decimal("1.2345"), "BHD") == 1235


def test_from_minor_for_zero_decimal_currency():
    assert from_minor(1250, "JPY") == Decimal("1250")


def test_split_evenly_distributes_the_remainder():
    assert split_evenly(10, 3, "USD") == [4, 3, 3]


def test_split_evenly_with_no_remainder():
    assert split_evenly(9, 3, "USD") == [3, 3, 3]


def test_split_evenly_rejects_zero_parts():
    with pytest.raises(ValueError):
        split_evenly(10, 0, "USD")


def test_split_evenly_validates_the_currency():
    with pytest.raises(UnsupportedCurrencyError):
        split_evenly(10, 2, "XYZ")


def test_format_amount_uses_a_known_symbol():
    assert format_amount(1234, "USD") == "$12.34"


def test_format_amount_for_zero_decimal_currency():
    assert format_amount(1250, "JPY") == "\u00a51250"


def test_format_amount_falls_back_to_the_code():
    assert format_amount(1234, "CAD") == "12.34 CAD"


def test_truncate_discards_the_remainder():
    assert truncate_to_minor(Decimal("10.009"), "USD") == 1000


def test_truncate_for_zero_decimal_currency():
    assert truncate_to_minor(Decimal("1250.9"), "JPY") == 1250
