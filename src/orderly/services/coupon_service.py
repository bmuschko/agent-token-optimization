"""Business rules for coupon records."""
from typing import Any, Dict, List

from orderly.errors import NotFoundError, ValidationError
from orderly.models.coupon import Coupon
from orderly.repositories.coupon_repository import CouponRepository


class CouponService:
    """Coordinates coupon reads and writes."""

    def __init__(self, repository: CouponRepository) -> None:
        self.repository = repository

    def create(self, payload: Dict[str, Any]) -> Coupon:
        """Validate and store a new coupon."""
        self._validate(payload)
        return self.repository.add(Coupon.from_dict(payload))

    def fetch(self, record_id: str) -> Coupon:
        """Read one record, raising when it is missing."""
        record = self.repository.get(record_id)
        if record is None:
            raise NotFoundError(f"no coupon with id {record_id}")
        return record

    def list_all(self) -> List[Dict[str, Any]]:
        """Every record, serialized."""
        return [r.to_dict() for r in self.repository.all()]

    def delete(self, record_id: str) -> bool:
        """Remove a record."""
        return self.repository.remove(record_id)

    @staticmethod
    def _validate(payload: Dict[str, Any]) -> None:
        """Reject payloads missing an id or code."""
        if not payload.get("id"):
            raise ValidationError("id", "is required")
        if not payload.get("code"):
            raise ValidationError("code", "is required")
