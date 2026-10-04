"""Volume discount tiers. Reference solution for T1.

Tiers are inclusive of their threshold: an order of exactly $100.00 earns
the 5% rate, not the rate below it.
"""
from typing import List, Tuple

# (threshold in whole currency units, discount rate)
TIERS: List[Tuple[int, float]] = [
    (0, 0.00),
    (100, 0.05),
    (500, 0.10),
    (1000, 0.15),
    (5000, 0.20),
]


def rate_for_subtotal(subtotal_cents: int) -> float:
    """Return the discount rate that applies to a subtotal in cents."""
    if subtotal_cents < 0:
        raise ValueError("subtotal_cents must not be negative")
    rate = 0.0
    for threshold, tier_rate in TIERS:
        if subtotal_cents >= threshold * 100:
            rate = tier_rate
    return rate


def discount_cents(subtotal_cents: int) -> int:
    """Return the discount owed on a subtotal, in cents, rounded down."""
    return int(subtotal_cents * rate_for_subtotal(subtotal_cents))


def total_after_discount(subtotal_cents: int) -> int:
    """Return the payable total after the volume discount is applied."""
    return subtotal_cents - discount_cents(subtotal_cents)


def describe_tier(subtotal_cents: int) -> str:
    """Human readable description of the tier a subtotal falls into."""
    rate = rate_for_subtotal(subtotal_cents)
    if rate == 0.0:
        return "no volume discount"
    return f"{int(rate * 100)}% volume discount"
