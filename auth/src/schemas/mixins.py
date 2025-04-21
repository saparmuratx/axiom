import datetime
from pydantic import ConfigDict
from pydantic.types import UUID4


class UUIDTimeStampMixin:
    id: UUID4
    created_at: datetime
    updated_at: datetime