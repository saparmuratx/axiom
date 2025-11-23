from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, UUID, Uuid, inspect
from sqlalchemy.exc import MissingGreenlet
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from axiom.models.exceptions import NotEagerLoadedError


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

        try:
            data = {attr: getattr(self, attr) for attr in attributes}
        except MissingGreenlet:
            raise NotEagerLoadedError(
                "SQLAlchemy model instance was not eagerly loaded. "
                "Call `await your_instance.eager_load(session)` to eagerly load relationships."
            ) from None
        else:
            return data


class AsyncEagerLoadingMixin:
    async def eager_load(self, session: AsyncSession, depth: int = 1):
        """
        Eagerly load relationships.
        depth=1: Load relationships as model instances.
        depth=0: Load only IDs (foreign key or list of IDs).
        Returns self.
        """

        mapper = inspect(type(self))
        relationships = mapper.relationships.keys()

        for rel in relationships:

            state = inspect(self)
            if rel not in state.unloaded:
                continue

            attr = await getattr(self.awaitable_attrs, rel)

            setattr(self, rel, attr)

            if depth == 0:
                if isinstance(attr, list):
                    id_list = [str(obj.id) for obj in attr]
                    setattr(self, f"{rel}_ids", id_list)

        return self
