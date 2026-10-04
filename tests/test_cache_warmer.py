"""Warmer behaviour on the single-threaded path.

The safety net for T8: whatever locking the fix introduces, these must hold.
"""
from orderly.cache.warmer import CacheWarmer


def fast_loader(key):
    """An immediate loader, no sleeping."""
    return {"sku": key}


def test_single_key_loads_once():
    warmer = CacheWarmer(fast_loader, workers=1)
    warmer.warm(["SKU-1"])
    assert warmer.load_count == 1


def test_entries_are_keyed_by_input():
    warmer = CacheWarmer(fast_loader, workers=1)
    warmer.warm(["SKU-1", "SKU-2"])
    assert sorted(warmer.entries) == ["SKU-1", "SKU-2"]


def test_reset_clears_state():
    warmer = CacheWarmer(fast_loader, workers=1)
    warmer.warm(["SKU-1"])
    warmer.reset()
    assert warmer.entries == {} and warmer.load_count == 0
