from typing import Any, Generic, TypeVar, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import BaseModel

from axiom.repository.exceptions import NotFoundException

T = TypeVar("T")  # SQLAlchemy model
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class GenericRepository(Generic[T, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(
        self,
        model: type[T],
        session: Session,
        default_schema: Type[ReadSchema],
        create_schema: Type[CreateSchema] | None = None,
        read_schema: Type[ReadSchema] | None = None,
        update_schema: Type[UpdateSchema] | None = None,
    ):
        self.model = model
        self.session = session
        self.default_schema = default_schema
        self.create_schema = create_schema or default_schema
        self.read_schema = read_schema or default_schema
        self.update_schema = update_schema or default_schema

    def _get_by_id(self, id: str) -> T:
        obj = self.session.query(self.model).filter(self.model.id == id).first()

        if not obj:
            raise NotFoundException

        return obj

    def get_by_field(self, field_name: str, value) -> ReadSchema:
        obj = (
            self.session.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
        )

        if not obj:
            raise NotFoundException

        return self.read_schema.model_validate(obj, from_attributes=True)

    def create(self, data: CreateSchema):
        obj = self.model(**data.model_dump())
        self.session.add(obj)

        schema = self.create_schema.model_validate(obj, from_attributes=True)

        return schema

    def get(self, id: str) -> ReadSchema:
        obj = self._get_by_id(id)

        return self.read_schema.model_validate(obj, from_attributes=True)

    def update(self, id: str, data: UpdateSchema) -> ReadSchema:
        obj = self._get_by_id(id)

        for key, value in data.model_dump().items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return self.read_schema.model_validate(obj, from_attributes=True)

    def delete(self, id: str):
        obj = self._get_by_id(id)
        self.session.delete(obj)


class AsyncGenericRepository(Generic[T, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(
        self,
        model: type[T],
        session: AsyncSession,
        default_schema: Type[ReadSchema],
        create_schema: Type[CreateSchema] | None = None,
        read_schema: Type[ReadSchema] | None = None,
        update_schema: Type[UpdateSchema] | None = None,
        eager: bool = True,
    ):
        self.model = model
        self.session = session
        self.default_schema = default_schema
        self.create_schema = create_schema or default_schema
        self.read_schema = read_schema or default_schema
        self.update_schema = update_schema or default_schema
        self.eager = eager

    async def load_to_schema(
        self, obj: T, eager: bool | None = None, depth: int | None = None
    ):
        use_eager = eager if eager is not None else self.eager

        if use_eager and hasattr(obj, "eager_load"):
            await obj.eager_load(session=self.session, depth=depth)

        schema = self.read_schema.model_validate(obj, from_attributes=True)

        return schema

    async def _get_by_id(self, id: str) -> T:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalar_one_or_none()

        if not obj:
            raise NotFoundException

        return obj

    async def get_by_field(
        self, field_name: str, value: Any, eager: bool | None = None
    ) -> ReadSchema:
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, field_name) == value)
        )
        obj = result.scalar_one_or_none()

        if not obj:
            raise NotFoundException

        return await self.load_to_schema(obj, eager=eager)

    async def create(self, data: CreateSchema):
        obj = self.model(**data.model_dump())
        self.session.add(obj)

        schema = self.create_schema.model_validate(obj, from_attributes=True)

        return schema

    async def retrieve(self, id: str, eager: bool | None = None, depth: int | None = None) -> ReadSchema:
        obj = await self._get_by_id(id)

        return await self.load_to_schema(obj, eager=eager, depth=depth)

    async def list(
        self, *, filters: dict = None, eager: bool | None = None
    ) -> list[ReadSchema]:
        stmt = select(self.model)
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(self.model, field) == value)
        result = await self.session.execute(stmt)
        objs = result.scalars().all()
        return [await self.load_to_schema(obj, eager=eager) for obj in objs]

    async def update(
        self, id: str, data: UpdateSchema, eager: bool | None = None
    ) -> ReadSchema:
        obj = await self._get_by_id(id)

        for key, value in data.model_dump().items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return await self.load_to_schema(obj, eager=eager)

    async def delete(self, id: str):
        obj = await self._get_by_id(id)
        await self.session.delete(obj)
