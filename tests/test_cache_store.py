"""TTL cache behaviour."""
from orderly.cache.store import TTLCache


def test_set_then_get():
    cache = TTLCache(ttl_seconds=60)
    cache.set("a", 1)
    assert cache.get("a") == 1


def test_missing_key_is_none():
    assert TTLCache().get("nope") is None


def test_expired_entry_is_dropped():
    cache = TTLCache(ttl_seconds=-1)
    cache.set("a", 1)
    assert cache.get("a") is None


def test_clear_empties_the_cache():
    cache = TTLCache()
    cache.set("a", 1)
    cache.clear()
    assert len(cache) == 0
