"""T8 acceptance: the warmer loads each key exactly once.

Eight workers are handed the same key eight times. A warmer that checks
membership and then loads without holding a claim will load it repeatedly,
because every worker clears the check before the first load finishes.
"""
import time

from orderly.cache.warmer import CacheWarmer


def slow_loader(key):
    """A loader slow enough that workers overlap."""
    time.sleep(0.05)
    return {"sku": key, "loaded_at": time.monotonic()}


def test_duplicate_keys_load_once():
    warmer = CacheWarmer(slow_loader, workers=8)
    warmer.warm(["SKU-1"] * 8)
    assert warmer.load_count == 1


def test_distinct_keys_each_load_once():
    warmer = CacheWarmer(slow_loader, workers=8)
    keys = [f"SKU-{i}" for i in range(8)] * 2
    warmer.warm(keys)
    assert warmer.load_count == 8
    assert len(warmer.entries) == 8


def test_every_key_ends_up_cached():
    warmer = CacheWarmer(slow_loader, workers=4)
    warmer.warm(["SKU-A", "SKU-B"] * 4)
    assert sorted(warmer.entries) == ["SKU-A", "SKU-B"]
