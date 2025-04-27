from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4


class UUIDTimeStampMixin:
    id: UUID4
    created_at: datetime
    updated_at: datetime


class UUIDMixin:
    id: UUID4


class DBObjectMixin:
    _object: Any | None = None

    def refresh(self: BaseModel):
        if not self._object:
            return self

        data = self.model_validate(self._object).model_dump()

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self
