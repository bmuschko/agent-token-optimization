"""Feed parsing with complete records."""
import json

from orderly.ingest.parser import parse_csv_row, parse_json_feed, parse_record

COMPLETE = {
    "order_id": "ORD-1",
    "customer_id": "CUST-1",
    "notes": "leave at door",
    "gift_message": "happy birthday",
    "po_number": "PO-9",
    "coupon": "SAVE10",
    "lines": [{"sku": "A", "quantity": 2, "unit_price_cents": 500}],
}


def test_parse_record_keeps_required_fields():
    record = parse_record(COMPLETE)
    assert record["order_id"] == "ORD-1"
    assert record["customer_id"] == "CUST-1"


def test_parse_record_normalizes_lines():
    record = parse_record(COMPLETE)
    assert record["lines"][0]["quantity"] == 2


def test_parse_json_feed_reads_wrapper_object():
    raw = json.dumps({"orders": [COMPLETE]})
    assert len(parse_json_feed(raw)) == 1


def test_parse_csv_row_blanks_become_none():
    record = parse_csv_row(["order_id", "customer_id", "notes"], ["ORD-2", "CUST-2", ""])
    assert record["notes"] is None
