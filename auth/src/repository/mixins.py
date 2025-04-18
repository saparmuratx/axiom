from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String,  DateTime, UUID, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


def generate_uuid():
    return str(uuid4())


class BaseModelMixin:
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True, server_default=func.now(), onupdate=func.now())


class SerializerMixin:
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
