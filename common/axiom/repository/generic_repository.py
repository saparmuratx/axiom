import importlib
from typing import Any, Generic, TypeVar, Type

from sqlalchemy import inspect
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from axiom.repository.exceptions import NotFoundException

T = TypeVar("T")  # SQLAlchemy model


class GenericRepository(Generic[T]):
    def __init__(
        self,
        model: type[T],
        session: Session,
    ):
        self.model = model
        self.session = session

    def _get_by_id(self, id: str) -> T:
        obj = self.session.query(self.model).filter(self.model.id == id).first()

        if not obj:
            raise NotFoundException

        return obj

    def get_by_field(self, field_name: str, value) -> T:
        obj = (
            self.session.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
        )

        if not obj:
            raise NotFoundException

        return self.read_schema.model_validate(obj, from_attributes=True)

    def create(self, data: dict):
        obj = self.model(**data.model_dump())
        self.session.add(obj)

        schema = self.create_schema.model_validate(obj, from_attributes=True)

        return schema

    def get(self, id: str) -> T:
        obj = self._get_by_id(id)

        return self.read_schema.model_validate(obj, from_attributes=True)

    def update(self, id: str, data: dict) -> T:
        obj = self._get_by_id(id)

        for key, value in data.model_dump().items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return self.read_schema.model_validate(obj, from_attributes=True)

    def delete(self, id: str) -> None:
        obj = self._get_by_id(id)
        self.session.delete(obj)


class AsyncGenericRepository(Generic[T]):
    def __init__(
        self,
        model: type[T],
        session: AsyncSession,
        eager: bool = True,
    ):
        self.model = model
        self.session = session
        self.eager = eager

    async def get_relationships(self):
        mapper = inspect(self.model)
        return list(mapper.relationships.keys())

    async def _get_by_id(self, id: str, eager: bool | None = None) -> T:
        use_eager = eager if eager is not None else self.eager

        stmt = select(self.model).where(self.model.id == id)

        if use_eager:
            relationships = await self.get_relationships()
            for rel in relationships:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)

        obj = result.scalar_one_or_none()

        if not obj:
            raise NotFoundException

        return obj

    async def get_by_field(
        self, field_name: str, value: Any, eager: bool | None = None
    ) -> T:
        use_eager = eager if eager is not None else self.eager

        stmt = select(self.model).where(getattr(self.model, field_name) == value)

        if use_eager:
            relationships = await self.get_relationships()
            for rel in relationships:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        result = await self.session.execute(stmt)

        obj = result.scalar_one_or_none()

        if not obj:
            raise NotFoundException

        return obj

    async def create(self, data: dict) -> T:
        obj = self.model(**data)

        self.session.add(obj)

        await self.session.flush()

        return obj

    async def retrieve(
        self, id: str, eager: bool | None = None, depth: int | None = None
    ) -> T:
        return await self._get_by_id(id, eager=eager)

    async def list(self, *, filters: dict = None, eager: bool | None = None) -> list[T]:
        stmt = select(self.model)

        use_eager = eager if eager is not None else self.eager

        relationships = await self.get_relationships()

        if use_eager:
            for rel in relationships:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)

        result = await self.session.execute(stmt)
        objs = result.scalars().all()

        return objs

    # TODO: optimize update operation
    async def update(self, id: str, data: dict, eager: bool | None = None) -> T:
        obj = await self._get_by_id(id, eager=False)

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        await self.session.flush()
        self.session.expire(obj)

        obj = await self._get_by_id(id, eager=eager)

        return obj

    async def delete(self, id: str) -> None:
        obj = await self._get_by_id(id)
        await self.session.delete(obj)
