"""Warehouse inventory client."""
import time

from orderly.config import settings
from orderly.errors import TransientError

WAREHOUSE_URL = "https://inventory.example.com"


class InventoryClient:
    """Stock levels and reservations."""

    def __init__(self, transport, attempts: int = None) -> None:
        self.transport = transport
        self.attempts = attempts or settings.retry_attempts

    def stock_for(self, sku: str) -> dict:
        """Read the stock level for a SKU, retrying transient failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.get(f"{WAREHOUSE_URL}/stock", {"sku": sku})
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error

    def reserve(self, sku: str, quantity: int) -> dict:
        """Reserve stock, retrying transient failures."""
        last_error = None
        delay = 0.1
        for attempt in range(self.attempts):
            try:
                return self.transport.post(
                    f"{WAREHOUSE_URL}/reservations",
                    {"sku": sku, "quantity": quantity},
                )
            except TransientError as exc:
                last_error = exc
                if attempt < self.attempts - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_error
