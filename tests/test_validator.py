"""Validation of complete records."""
import pytest

from orderly.errors import ValidationError
from orderly.ingest.validator import validate

VALID = {
    "order_id": "ORD-1",
    "customer_id": "CUST-1",
    "notes": "",
    "gift_message": "",
    "lines": [{"sku": "A", "quantity": 1, "unit_price_cents": 100}],
}


def test_valid_record_passes():
    assert validate(dict(VALID)) == VALID


def test_missing_order_id_is_rejected():
    record = dict(VALID, order_id=None)
    with pytest.raises(ValidationError):
        validate(record)


def test_empty_lines_are_rejected():
    record = dict(VALID, lines=[])
    with pytest.raises(ValidationError):
        validate(record)


def test_zero_quantity_is_rejected():
    record = dict(VALID, lines=[{"sku": "A", "quantity": 0, "unit_price_cents": 1}])
    with pytest.raises(ValidationError):
        validate(record)


def test_overlong_notes_are_rejected():
    record = dict(VALID, notes="x" * 501)
    with pytest.raises(ValidationError):
        validate(record)
