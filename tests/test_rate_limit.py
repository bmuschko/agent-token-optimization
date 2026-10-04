"""Rolling-window rate limiting."""
import pytest

from orderly.api.middleware.rate_limit import RateLimiter
from orderly.errors import RateLimitExceeded


def test_requests_under_the_limit_pass():
    limiter = RateLimiter(limit=3, window=60)
    for _ in range(3):
        limiter.check("client-a")


def test_request_over_the_limit_is_rejected():
    limiter = RateLimiter(limit=2, window=60)
    limiter.check("client-a")
    limiter.check("client-a")
    with pytest.raises(RateLimitExceeded):
        limiter.check("client-a")


def test_clients_are_tracked_separately():
    limiter = RateLimiter(limit=1, window=60)
    limiter.check("client-a")
    limiter.check("client-b")


def test_remaining_counts_down():
    limiter = RateLimiter(limit=5, window=60)
    limiter.check("client-a")
    assert limiter.remaining("client-a") == 4
