"""Validate parsed records before they reach the order service."""
from typing import Any, Dict

from orderly.errors import ValidationError

MAX_NOTES_LENGTH = 500
MAX_GIFT_MESSAGE_LENGTH = 200
MAX_LINES = 100


def validate(record: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a parsed record, returning it unchanged when it is sound."""
    for field in ("order_id", "customer_id"):
        if not record.get(field):
            raise ValidationError(field, "is required")

    lines = record.get("lines") or []
    if not lines:
        raise ValidationError("lines", "at least one line is required")
    if len(lines) > MAX_LINES:
        raise ValidationError("lines", f"no more than {MAX_LINES} lines")
    for index, line in enumerate(lines):
        _validate_line(index, line)

    _validate_text(record, "notes", MAX_NOTES_LENGTH)
    _validate_text(record, "gift_message", MAX_GIFT_MESSAGE_LENGTH)
    return record


def _validate_line(index: int, line: Dict[str, Any]) -> None:
    """Validate a single line item."""
    if not line.get("sku"):
        raise ValidationError(f"lines[{index}].sku", "is required")
    if line.get("quantity", 0) <= 0:
        raise ValidationError(f"lines[{index}].quantity", "must be positive")
    if line.get("unit_price_cents", 0) < 0:
        raise ValidationError(f"lines[{index}].unit_price_cents", "must not be negative")


def _validate_text(record: Dict[str, Any], field: str, limit: int) -> None:
    """Validate an optional free-text field against a length limit."""
    value = record.get(field)
    if len(value) > limit:
        raise ValidationError(field, f"must be {limit} characters or fewer")
