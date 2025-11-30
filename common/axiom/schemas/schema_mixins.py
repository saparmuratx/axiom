from datetime import datetime
from pydantic.types import UUID4


class TimeStampMixin:
    created_at: datetime
    updated_at: datetime


class UUIDMixin:
    id: UUID4


class UUIDTimeStampMixin:
    id: UUID4
    created_at: datetime
    updated_at: datetime
