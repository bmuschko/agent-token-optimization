"""T3 acceptance: omitted optional fields survive validation."""
from orderly.ingest.parser import parse_record
from orderly.ingest.validator import validate

MINIMAL = {
    "order_id": "ORD-1",
    "customer_id": "CUST-1",
    "lines": [{"sku": "A", "quantity": 1, "unit_price_cents": 100}],
}


def test_record_without_notes_validates():
    validate(parse_record(MINIMAL))


def test_record_with_explicit_none_validates():
    validate(parse_record(dict(MINIMAL, notes=None, gift_message=None)))


def test_long_notes_are_still_rejected():
    import pytest

    from orderly.errors import ValidationError

    with pytest.raises(ValidationError):
        validate(parse_record(dict(MINIMAL, notes="x" * 501)))
