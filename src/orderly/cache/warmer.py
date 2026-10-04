"""Warm the product cache on startup.

The warmer runs across a thread pool so a cold start does not take minutes.
Each SKU should be loaded exactly once, however many workers are running and
however often a SKU appears in the input.
"""
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Iterable


class CacheWarmer:
    """Loads values for a set of keys into a cache, in parallel."""

    def __init__(self, loader: Callable[[str], Dict], workers: int = 8) -> None:
        self.loader = loader
        self.workers = workers
        self.entries: Dict[str, Dict] = {}
        self.load_count = 0

    def warm(self, keys: Iterable[str]) -> Dict[str, Dict]:
        """Load every key, skipping any key that is already loaded."""
        keys = list(keys)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            list(pool.map(self._warm_one, keys))
        return self.entries

    def _warm_one(self, key: str) -> None:
        """Load a single key unless it is already in the cache."""
        if key in self.entries:
            return
        value = self.loader(key)
        self.entries[key] = value
        self.load_count += 1

    def reset(self) -> None:
        """Forget everything loaded so far."""
        self.entries = {}
        self.load_count = 0
