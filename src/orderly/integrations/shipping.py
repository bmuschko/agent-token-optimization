"""Shipping carrier client."""
import time

from orderly.config import settings
from orderly.errors import TransientError

CARRIER_URL = "https://shipping.example.com/api"


class ShippingClient:
    """Rates and labels from the carrier."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def quote(self, postcode: str, weight_grams: int) -> dict:
        """Fetch a shipping quote, retrying transient carrier failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.get(
                    f"{CARRIER_URL}/rates",
                    {"postcode": postcode, "weight": weight_grams},
                )
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error

    def create_label(self, order_id: str, service: str) -> dict:
        """Buy a shipping label, retrying transient carrier failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.post(
                    f"{CARRIER_URL}/labels",
                    {"order_id": order_id, "service": service},
                )
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error
