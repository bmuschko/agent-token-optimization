"""Repository behaviour."""
from orderly.models.customer import Customer
from orderly.repositories.customer_repository import CustomerRepository


def test_add_then_get():
    repo = CustomerRepository()
    repo.add(Customer(id="C1", email="a@example.com", name="A", tier="gold"))
    assert repo.get("C1").email == "a@example.com"


def test_find_by_first_field():
    repo = CustomerRepository([Customer(id="C1", email="a@example.com")])
    assert len(repo.find_by_email("a@example.com")) == 1


def test_remove_reports_existence():
    repo = CustomerRepository([Customer(id="C1")])
    assert repo.remove("C1") is True
    assert repo.remove("C1") is False
