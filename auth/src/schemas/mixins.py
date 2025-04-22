from datetime import datetime
from typing import Any
from pydantic import ConfigDict
from pydantic.types import UUID4


class UUIDTimeStampMixin:
    id: UUID4 | None
    created_at: datetime | None
    updated_at: datetime | None


class DBObjectMixin:
    _object: Any | None = None
