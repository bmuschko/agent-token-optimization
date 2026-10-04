"""Regional tax rates."""
from orderly.pricing.tax import rate_for_region, tax_cents


def test_known_region():
    assert rate_for_region("US-CO") == 0.029


def test_region_is_case_insensitive():
    assert rate_for_region("us-co") == 0.029


def test_unknown_region_is_untaxed():
    assert rate_for_region("XX") == 0.0


def test_tax_rounds_to_nearest_cent():
    assert tax_cents(10_000, "US-CO") == 290
