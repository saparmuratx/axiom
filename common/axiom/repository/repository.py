from typing import Any, Generic, TypeVar, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from pydantic import BaseModel

from axiom.repository.repository_exceptions import NotFoundException

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
        obj = self.session.query(self.model).filter(getattr(self.model, field_name) == value).first()
        if not obj:
            raise NotFoundException
        return self.read_schema.model_validate(obj)

    def create(self, data: CreateSchema):
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        schema = self.create_schema.model_validate(obj, from_attributes=True)
        schema._object = obj
        return schema

    def get(self, id: str) -> ReadSchema:
        obj = self._get_by_id(id)
        return self.read_schema.model_validate(obj)

    def update(self, id: str, data: UpdateSchema) -> ReadSchema:
        obj = self._get_by_id(id)
        for key, value in data.model_dump().items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return self.read_schema.model_validate(obj)

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
    ):
        self.model = model
        self.session = session
        self.default_schema = default_schema
        self.create_schema = create_schema or default_schema
        self.read_schema = read_schema or default_schema
        self.update_schema = update_schema or default_schema

    async def _get_by_id(self, id: str) -> T:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalar_one_or_none()
        if not obj:
            raise NotFoundException
        return obj

    async def get_by_field(self, field_name: str, value: Any) -> ReadSchema:
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, field_name) == value)
        )
        obj = result.scalar_one_or_none()
        if not obj:
            raise NotFoundException
        return self.read_schema.model_validate(obj)

    async def create(self, data: CreateSchema):
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        # Optionally: await self.session.flush() to get PKs
        schema = self.create_schema.model_validate(obj, from_attributes=True)
        schema._object = obj
        return schema

    async def get(self, id: str) -> ReadSchema:
        obj = await self._get_by_id(id)
        return self.read_schema.model_validate(obj)

    async def update(self, id: str, data: UpdateSchema) -> ReadSchema:
        obj = await self._get_by_id(id)
        for key, value in data.model_dump().items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return self.read_schema.model_validate(obj)

    async def delete(self, id: str):
        obj = await self._get_by_id(id)
        await self.session.delete(obj)