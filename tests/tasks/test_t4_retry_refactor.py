"""T4 acceptance: the retry loop exists in one place, not three.

Behaviour is covered by tests/test_integrations.py. This file only checks
that the duplication is gone.
"""
import inspect
import re

from orderly.integrations import inventory, payments, shipping

MODULES = (payments, shipping, inventory)
RETRY_LOOP = re.compile(r"for attempt in range\(")
SLEEP_CALL = re.compile(r"time\.sleep\(")


def test_no_module_hand_rolls_a_retry_loop():
    offenders = [m.__name__ for m in MODULES
                 if RETRY_LOOP.search(inspect.getsource(m))]
    assert offenders == [], f"retry loop still inline in: {offenders}"


def test_no_module_sleeps_directly():
    offenders = [m.__name__ for m in MODULES
                 if SLEEP_CALL.search(inspect.getsource(m))]
    assert offenders == [], f"backoff still inline in: {offenders}"


def test_clients_still_expose_their_methods():
    assert hasattr(payments.PaymentClient, "charge")
    assert hasattr(payments.PaymentClient, "refund")
    assert hasattr(shipping.ShippingClient, "quote")
    assert hasattr(inventory.InventoryClient, "reserve")
