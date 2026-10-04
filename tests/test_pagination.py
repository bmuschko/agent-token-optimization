"""Pagination helpers."""
from orderly.utils.pagination import clamp_limit, clamp_offset, page


def test_clamp_limit_defaults_on_garbage():
    assert clamp_limit("abc") == 25


def test_clamp_limit_caps_at_max():
    assert clamp_limit(10_000) == 200


def test_clamp_offset_floors_at_zero():
    assert clamp_offset(-5) == 0


def test_page_reports_the_window():
    result = page(list(range(10)), limit=3, offset=3)
    assert result["items"] == [3, 4, 5]
    assert result["total"] == 10
    assert result["has_more"] is True
