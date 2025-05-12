from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, UUID, Uuid, inspect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModelMixin:
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SerializerMixin:
    def to_dict(self):
        columns = [column.name for column in self.__table__.columns]
        mapper = inspect(type(self))

        attributes = columns + list(mapper.relationships.keys())

        return {attr: getattr(self, attr) for attr in attributes}
