"""Exception hierarchy for the service."""


class OrderlyError(Exception):
    """Base class for every error this package raises."""


class ValidationError(OrderlyError):
    """Raised when an inbound record fails validation."""

    def __init__(self, field: str, reason: str) -> None:
        super().__init__(f"{field}: {reason}")
        self.field = field
        self.reason = reason


class UnsupportedCurrencyError(OrderlyError):
    """Raised when a currency code has no configured rounding rule."""


class RateLimitExceeded(OrderlyError):
    """Raised when a client exceeds its allowance for the current window."""


class TransientError(OrderlyError):
    """Raised by integrations for failures that are worth retrying."""


class NotFoundError(OrderlyError):
    """Raised when a record does not exist."""
