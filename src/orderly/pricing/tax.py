"""Flat regional tax rates. Real systems use a tax service; this is enough."""

RATES = {
    "US-CO": 0.029,
    "US-CA": 0.0725,
    "US-NY": 0.04,
    "DE": 0.19,
    "GB": 0.20,
    "JP": 0.10,
}
DEFAULT_RATE = 0.0


def rate_for_region(region: str) -> float:
    """Return the tax rate for a region code, defaulting to zero."""
    return RATES.get(region.upper(), DEFAULT_RATE)


def tax_cents(taxable_cents: int, region: str) -> int:
    """Tax owed on a taxable amount, rounded to the nearest cent."""
    return round(taxable_cents * rate_for_region(region))
