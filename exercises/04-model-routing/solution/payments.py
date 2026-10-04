"""Payment gateway client. Reference solution for T4."""
from orderly.config import settings
from orderly.errors import TransientError
from orderly.utils.retry import call_with_retry

GATEWAY_URL = "https://payments.example.com/v2"


class PaymentClient:
    """Charges and refunds against the payment gateway."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def charge(self, order_id: str, amount_cents: int, currency: str) -> dict:
        """Charge an order, retrying transient gateway failures."""
        return call_with_retry(
            lambda: self.transport.post(
                f"{GATEWAY_URL}/charges",
                {"order_id": order_id, "amount": amount_cents, "currency": currency},
            ),
            attempts=self.attempts,
            retry_on=TransientError,
        )

    def refund(self, charge_id: str, amount_cents: int) -> dict:
        """Refund a charge, retrying transient gateway failures."""
        return call_with_retry(
            lambda: self.transport.post(
                f"{GATEWAY_URL}/refunds",
                {"charge_id": charge_id, "amount": amount_cents},
            ),
            attempts=self.attempts,
            retry_on=TransientError,
        )
