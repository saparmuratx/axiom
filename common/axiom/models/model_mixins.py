from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, UUID, Uuid, inspect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.sql import select


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



class AsyncSerializerAlternativeMixin:
    async def to_dict(self):
        """
        Convert the ORM model instance to a dict.
        Only includes relationships if already loaded.
        """
        columns = [column.name for column in self.__table__.columns]
        mapper = sa_inspect(type(self))
        relationships = set(mapper.relationships.keys())
        data = {}

        for col in columns:
            data[col] = str(getattr(self, col))

        # Only include relationships if already loaded
        state = sa_inspect(self)
        for rel in relationships:
            if rel in state.unloaded:
                data[rel] = None
            else:
                value = getattr(self, rel)
                if isinstance(value, list):
                    data[rel] = [str(getattr(obj, "id", None)) for obj in value]
                elif value is not None:
                    data[rel] = str(getattr(value, "id", value))
                else:
                    data[rel] = None

        return data



class AsyncEagerLoadingAlternativeMixin:
    async def eager_load(self, session: AsyncSession = None, depth: int = 1):
        """
        Eagerly load relationships. 
        depth=1: Load relationships as model instances.
        depth=0: Load only IDs (foreign key or list of IDs).
        Returns self.
        """
        if not session:
            return self

        mapper = sa_inspect(type(self))
        relationships = mapper.relationships.keys()

        for rel in relationships:
            state = sa_inspect(self)
            if rel not in state.unloaded:
                continue

            attr = await getattr(self.awaitable_attrs, rel)

            setattr(self, rel, attr)

            if depth == 0:
                if isinstance(attr, list):
                    id_list = [str(obj.id) for obj in attr]
                    setattr(self, f"{rel}_ids", id_list)


        return self
                    

class AsyncEagerLoadingSerailizerAlternativeMixin(AsyncEagerLoadingAlternativeMixin, AsyncSerializerAlternativeMixin):
    pass
