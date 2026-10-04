"""Retry behaviour across the integration clients.

This is the safety net for the T4 refactor: the behaviour below must not
change, however the retry logic is organized.
"""
import pytest

from orderly.errors import TransientError
from orderly.integrations.inventory import InventoryClient
from orderly.integrations.payments import PaymentClient
from orderly.integrations.shipping import ShippingClient
from orderly.integrations.transport import RecordingTransport


def test_charge_succeeds_first_time():
    transport = RecordingTransport([{"id": "ch_1"}])
    assert PaymentClient(transport).charge("ORD-1", 100, "USD") == {"id": "ch_1"}


def test_charge_retries_transient_failures():
    transport = RecordingTransport([TransientError("boom"), {"id": "ch_2"}])
    client = PaymentClient(transport, attempts=3)
    assert client.charge("ORD-1", 100, "USD") == {"id": "ch_2"}
    assert len(transport.calls) == 2


def test_charge_gives_up_after_the_last_attempt():
    transport = RecordingTransport([TransientError("a"), TransientError("b")])
    client = PaymentClient(transport, attempts=2)
    with pytest.raises(TransientError):
        client.charge("ORD-1", 100, "USD")
    assert len(transport.calls) == 2


def test_shipping_quote_retries():
    transport = RecordingTransport([TransientError("x"), {"rate": 500}])
    client = ShippingClient(transport, attempts=2)
    assert client.quote("80211", 1000) == {"rate": 500}


def test_inventory_reserve_retries():
    transport = RecordingTransport([TransientError("x"), {"reserved": True}])
    client = InventoryClient(transport, attempts=2)
    assert client.reserve("SKU-1", 2) == {"reserved": True}
