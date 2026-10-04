"""Currency formatting and rounding.

Most currencies use two minor units. A few use none, and a few use three.
Rounding has to respect that or totals drift by a unit.
"""
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from orderly.errors import UnsupportedCurrencyError

ZERO_DECIMAL = {"JPY", "KRW", "VND", "CLP"}
THREE_DECIMAL = {"BHD", "KWD", "OMR", "TND"}
TWO_DECIMAL = {"USD", "EUR", "GBP", "CAD", "AUD", "CHF", "SEK", "NOK"}

SYMBOLS = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3", "JPY": "\u00a5"}


def minor_units(code: str) -> int:
    """Return how many minor units a currency code uses."""
    code = code.upper()
    if code in ZERO_DECIMAL:
        return 0
    if code in THREE_DECIMAL:
        return 3
    if code in TWO_DECIMAL:
        return 2
    raise UnsupportedCurrencyError(f"unknown currency: {code}")


def to_minor(amount: Decimal, code: str) -> int:
    """Convert a decimal amount into whole minor units."""
    places = minor_units(code)
    quantum = Decimal(1).scaleb(-places)
    rounded = amount.quantize(quantum, rounding=ROUND_HALF_UP)
    return int(rounded.scaleb(places))


def from_minor(units: int, code: str) -> Decimal:
    """Convert whole minor units back into a decimal amount."""
    places = minor_units(code)
    return Decimal(units).scaleb(-places)


def split_evenly(units: int, parts: int, code: str) -> list:
    """Split minor units into parts, giving remainder to the earliest parts."""
    if parts <= 0:
        raise ValueError("parts must be positive")
    minor_units(code)  # validates the code
    base, remainder = divmod(units, parts)
    return [base + (1 if i < remainder else 0) for i in range(parts)]


def format_amount(units: int, code: str) -> str:
    """Format minor units for display, with a symbol when one is known."""
    code = code.upper()
    amount = from_minor(units, code)
    places = minor_units(code)
    if places == 0:
        text = f"{amount:.0f}"
    else:
        text = f"{amount:.{places}f}"
    symbol = SYMBOLS.get(code)
    if symbol:
        return f"{symbol}{text}"
    return f"{text} {code}"


def truncate_to_minor(amount: Decimal, code: str) -> int:
    """Convert to minor units, discarding the remainder instead of rounding."""
    places = minor_units(code)
    quantum = Decimal(1).scaleb(-places)
    return int(amount.quantize(quantum, rounding=ROUND_DOWN).scaleb(places))
