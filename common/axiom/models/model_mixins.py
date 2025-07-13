from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, UUID, Uuid, inspect
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect as sa_inspect


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


class AsyncSerializerMixin:
    async def to_dict(
        self, session: AsyncSession = None, load_relationships: bool = True
    ):
        """
        Convert the ORM model instance to a dict, with async support for relationships.
        If session is provided and load_relationships is True, eagerly loads all relationships.
        """
        columns = [column.name for column in self.__table__.columns]
        mapper = sa_inspect(type(self))
        relationships = list(mapper.relationships.keys())
        data = {col: getattr(self, col) for col in columns}

        if session and load_relationships:
            # Eagerly load all relationships if not already loaded
            for rel in relationships:
                state = sa_inspect(self)
                if rel in state.unloaded:
                    await session.refresh(self, [rel])
                value = getattr(self, rel)
                if isinstance(value, list):
                    data[rel] = [getattr(obj, "id", obj) for obj in value]
                elif value is not None:
                    data[rel] = getattr(value, "id", value)
                else:
                    data[rel] = None
        else:
            # Only include relationships if already loaded
            for rel in relationships:
                state = sa_inspect(self)
                if rel in state.unloaded:
                    data[rel] = None
                else:
                    value = getattr(self, rel)
                    if isinstance(value, list):
                        data[rel] = [getattr(obj, "id", obj) for obj in value]
                    elif value is not None:
                        data[rel] = getattr(value, "id", value)
                    else:
                        data[rel] = None
        return data


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
            data[col] = getattr(self, col)

        # Only include relationships if already loaded
        state = sa_inspect(self)
        for rel in relationships:
            if rel in state.unloaded:
                data[rel] = None
            else:
                value = getattr(self, rel)
                if isinstance(value, list):
                    data[rel] = [getattr(obj, "id", obj) for obj in value]
                elif value is not None:
                    data[rel] = getattr(value, "id", value)
                else:
                    data[rel] = None

        return data


class AsyncEagerLoadingMixin:
    async def eager_load(
        self, session: AsyncSession = None
    ):
        """
        Eagerly load all relationships and set them as attributes on the instance.
        Returns self.
        """

        if not session:
            return self

        mapper = sa_inspect(type(self))
        relationships = list(mapper.relationships.keys())

        for rel in relationships:
            
            print(rel)

            state = sa_inspect(self)
            if rel in state.unloaded:
                await session.refresh(self, [rel])
            
        return self


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
            if depth == 1:
                await session.refresh(self, [rel])
            elif depth == 0:
                rel_prop = mapper.relationships[rel]
                if rel_prop.uselist:
                    result = await session.execute(rel_prop.table.select().where(rel_prop.primaryjoin))
                    setattr(self, f"{rel}_ids", [row[0] for row in result])
                else:
                    fk = next(iter(rel_prop.local_columns)).name
                    setattr(self, f"{rel}_id", getattr(self, fk))

        return self


class AsyncEagerLoadingSerailizerMixin(AsyncEagerLoadingMixin, AsyncSerializerAlternativeMixin):
    pass


class AsyncEagerLoadingSerailizerAlternativeMixin(AsyncEagerLoadingAlternativeMixin, AsyncSerializerAlternativeMixin):
    pass
