"""Payment gateway client."""
import time

from orderly.config import settings
from orderly.errors import TransientError

GATEWAY_URL = "https://payments.example.com/v2"


class PaymentClient:
    """Charges and refunds against the payment gateway."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def charge(self, order_id: str, amount_cents: int, currency: str) -> dict:
        """Charge an order, retrying transient gateway failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.post(
                    f"{GATEWAY_URL}/charges",
                    {"order_id": order_id, "amount": amount_cents, "currency": currency},
                )
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error

    def refund(self, charge_id: str, amount_cents: int) -> dict:
        """Refund a charge, retrying transient gateway failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.post(
                    f"{GATEWAY_URL}/refunds",
                    {"charge_id": charge_id, "amount": amount_cents},
                )
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error
