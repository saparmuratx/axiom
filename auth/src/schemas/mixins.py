import datetime
from pydantic import ConfigDict
from pydantic.types import UUID4


class UUIDTimeStampMixin:
    id: UUID4 | None
    created_at: str | None
    updated_at: str | None
