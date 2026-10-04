"""Parse inbound order records from partner feeds.

Partners send CSV rows and JSON objects with wildly inconsistent optional
fields. Everything optional comes through as None when the partner omits it.
"""
import json
from typing import Any, Dict, Iterable, List

OPTIONAL_FIELDS = ("notes", "gift_message", "po_number", "coupon")
REQUIRED_FIELDS = ("order_id", "customer_id", "lines")


def parse_json_feed(raw: str) -> List[Dict[str, Any]]:
    """Parse a JSON feed into a list of records."""
    payload = json.loads(raw)
    if isinstance(payload, dict):
        payload = payload.get("orders", [])
    return [parse_record(item) for item in payload]


def parse_record(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize one inbound record into the shape the validator expects."""
    record: Dict[str, Any] = {}
    for field in REQUIRED_FIELDS:
        record[field] = item.get(field)
    for field in OPTIONAL_FIELDS:
        record[field] = item.get(field)
    record["lines"] = _parse_lines(item.get("lines") or [])
    return record


def _parse_lines(lines: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize the line items on a record."""
    parsed = []
    for line in lines:
        parsed.append(
            {
                "sku": line.get("sku"),
                "quantity": int(line.get("quantity", 0)),
                "unit_price_cents": int(line.get("unit_price_cents", 0)),
            }
        )
    return parsed


def parse_csv_row(header: List[str], row: List[str]) -> Dict[str, Any]:
    """Parse a single CSV row using the feed header."""
    item = {key: (value if value != "" else None) for key, value in zip(header, row)}
    item["lines"] = []
    return parse_record(item)
