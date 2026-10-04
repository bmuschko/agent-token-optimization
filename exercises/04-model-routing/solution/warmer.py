"""Warm the product cache on startup. Reference solution for T8."""
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Iterable, Set


class CacheWarmer:
    """Loads values for a set of keys into a cache, in parallel."""

    def __init__(self, loader: Callable[[str], Dict], workers: int = 8) -> None:
        self.loader = loader
        self.workers = workers
        self.entries: Dict[str, Dict] = {}
        self.load_count = 0
        self._lock = threading.Lock()
        self._claimed: Set[str] = set()

    def warm(self, keys: Iterable[str]) -> Dict[str, Dict]:
        """Load every key, skipping any key already loaded or claimed."""
        keys = list(keys)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            list(pool.map(self._warm_one, keys))
        return self.entries

    def _warm_one(self, key: str) -> None:
        """Load a single key unless another worker already claimed it."""
        with self._lock:
            if key in self.entries or key in self._claimed:
                return
            self._claimed.add(key)
        value = self.loader(key)
        with self._lock:
            self.entries[key] = value
            self.load_count += 1

    def reset(self) -> None:
        """Forget everything loaded so far."""
        with self._lock:
            self.entries = {}
            self._claimed = set()
            self.load_count = 0
