"""Shared fixtures."""
import pytest

from orderly.integrations.transport import RecordingTransport
from orderly.repositories.order_repository import OrderRepository
from orderly.seed import load_seed_orders


@pytest.fixture
def seed_orders():
    """A deterministic set of orders."""
    return load_seed_orders()


@pytest.fixture
def order_repository(seed_orders):
    """A repository preloaded with seed orders."""
    return OrderRepository(seed_orders)


@pytest.fixture
def transport():
    """A transport that records calls and replays scripted responses."""
    return RecordingTransport()
