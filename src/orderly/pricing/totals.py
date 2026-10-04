"""Order total assembly."""
from orderly.pricing.discount import discount_cents
from orderly.pricing.tax import tax_cents


def line_subtotal(unit_price_cents: int, quantity: int) -> int:
    """Subtotal for a single line."""
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    return unit_price_cents * quantity


def order_subtotal(lines) -> int:
    """Sum of every line subtotal on an order."""
    return sum(line_subtotal(l["unit_price_cents"], l["quantity"]) for l in lines)


def order_total(lines, region: str = "US-CO") -> dict:
    """Full breakdown for an order: subtotal, discount, tax and total."""
    subtotal = order_subtotal(lines)
    discount = discount_cents(subtotal)
    taxable = subtotal - discount
    tax = tax_cents(taxable, region)
    return {
        "subtotal_cents": subtotal,
        "discount_cents": discount,
        "tax_cents": tax,
        "total_cents": taxable + tax,
    }
