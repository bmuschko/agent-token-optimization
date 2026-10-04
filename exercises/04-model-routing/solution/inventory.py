"""Warehouse inventory client. Reference solution for T4."""
from orderly.config import settings
from orderly.errors import TransientError
from orderly.utils.retry import call_with_retry

WAREHOUSE_URL = "https://inventory.example.com"


class InventoryClient:
    """Stock levels and reservations."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def stock_for(self, sku: str) -> dict:
        """Read the stock level for a SKU, retrying transient failures."""
        return call_with_retry(
            lambda: self.transport.get(f"{WAREHOUSE_URL}/stock", {"sku": sku}),
            attempts=self.attempts,
            retry_on=TransientError,
        )

    def reserve(self, sku: str, quantity: int) -> dict:
        """Reserve stock, retrying transient failures."""
        return call_with_retry(
            lambda: self.transport.post(
                f"{WAREHOUSE_URL}/reservations", {"sku": sku, "quantity": quantity}
            ),
            attempts=self.attempts,
            retry_on=TransientError,
        )
