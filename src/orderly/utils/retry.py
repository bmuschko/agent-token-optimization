"""Retry helpers.

Nothing in integrations/ uses this yet. It is here as a seam.
"""
import time
from typing import Callable, Iterable, Type


def backoff_delays(attempts: int, base: float = 0.1) -> Iterable[float]:
    """Yield exponential backoff delays for a number of attempts."""
    delay = base
    for _ in range(max(0, attempts - 1)):
        yield delay
        delay *= 2


def call_with_retry(func: Callable, attempts: int, retry_on: Type[Exception],
                    base_delay: float = 0.1):
    """Call a function, retrying a named exception with exponential backoff."""
    last_error = None
    delays = list(backoff_delays(attempts, base_delay))
    for attempt in range(attempts):
        try:
            return func()
        except retry_on as exc:
            last_error = exc
            if attempt < len(delays):
                time.sleep(delays[attempt])
    raise last_error
