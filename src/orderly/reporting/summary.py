"""Order summary reports."""
from typing import Any, Dict, List, Optional

from orderly.pricing.totals import order_total


def build_summary(orders: List[Dict[str, Any]], status: Optional[str] = None,
                  region: str = "US-CO") -> Dict[str, Any]:
    """Build a summary over a set of orders."""
    selected = [o for o in orders if status is None or o["status"] == status]
    totals = [order_total(o["lines"], region) for o in selected]
    return {
        "order_count": len(selected),
        "status": status or "all",
        "region": region,
        "subtotal_cents": sum(t["subtotal_cents"] for t in totals),
        "discount_cents": sum(t["discount_cents"] for t in totals),
        "tax_cents": sum(t["tax_cents"] for t in totals),
        "total_cents": sum(t["total_cents"] for t in totals),
    }


def render_text(summary: Dict[str, Any]) -> str:
    """Render a summary as aligned plain text."""
    lines = [
        f"Orders   : {summary['order_count']}",
        f"Status   : {summary['status']}",
        f"Region   : {summary['region']}",
        f"Subtotal : {summary['subtotal_cents'] / 100:.2f}",
        f"Discount : {summary['discount_cents'] / 100:.2f}",
        f"Tax      : {summary['tax_cents'] / 100:.2f}",
        f"Total    : {summary['total_cents'] / 100:.2f}",
    ]
    return "\n".join(lines) + "\n"
