"""Shipping carrier client. Reference solution for T4."""
from orderly.config import settings
from orderly.errors import TransientError
from orderly.utils.retry import call_with_retry

CARRIER_URL = "https://shipping.example.com/api"


class ShippingClient:
    """Rates and labels from the carrier."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def quote(self, postcode: str, weight_grams: int) -> dict:
        """Fetch a shipping quote, retrying transient carrier failures."""
        return call_with_retry(
            lambda: self.transport.get(
                f"{CARRIER_URL}/rates", {"postcode": postcode, "weight": weight_grams}
            ),
            attempts=self.attempts,
            retry_on=TransientError,
        )

    def create_label(self, order_id: str, service: str) -> dict:
        """Buy a shipping label, retrying transient carrier failures."""
        return call_with_retry(
            lambda: self.transport.post(
                f"{CARRIER_URL}/labels", {"order_id": order_id, "service": service}
            ),
            attempts=self.attempts,
            retry_on=TransientError,
        )
