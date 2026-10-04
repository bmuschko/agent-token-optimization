"""T1 acceptance: tier thresholds are inclusive."""
from orderly.pricing.discount import rate_for_subtotal


def test_exactly_at_the_first_threshold_earns_the_tier():
    assert rate_for_subtotal(100_00) == 0.05


def test_exactly_at_the_second_threshold_earns_the_tier():
    assert rate_for_subtotal(500_00) == 0.10


def test_one_cent_below_a_threshold_stays_in_the_lower_tier():
    assert rate_for_subtotal(99_99) == 0.0
    assert rate_for_subtotal(499_99) == 0.05


def test_top_tier_is_reachable():
    assert rate_for_subtotal(5000_00) == 0.20
