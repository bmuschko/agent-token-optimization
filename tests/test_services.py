"""Service layer behaviour."""
import pytest

from orderly.errors import NotFoundError, ValidationError
from orderly.repositories.product_repository import ProductRepository
from orderly.services.product_service import ProductService


def service():
    return ProductService(ProductRepository())


def test_create_requires_an_id():
    with pytest.raises(ValidationError):
        service().create({"sku": "SKU-1"})


def test_create_then_fetch():
    svc = service()
    svc.create({"id": "P1", "sku": "SKU-1", "title": "Thing"})
    assert svc.fetch("P1").sku == "SKU-1"


def test_fetch_missing_raises():
    with pytest.raises(NotFoundError):
        service().fetch("nope")


def test_list_all_serializes():
    svc = service()
    svc.create({"id": "P1", "sku": "SKU-1"})
    assert svc.list_all()[0]["id"] == "P1"
