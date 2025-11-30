from math import ceil
from typing import Any, Generic, TypeVar

from sqlalchemy import inspect, Select, desc
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from axiom.repository.exceptions import NotFoundException
from axiom.repository.filter_map import FILTER_MAP

T = TypeVar("T")  # SQLAlchemy model


class GenericRepository(Generic[T]):
    def __init__(
        self,
        model: type[T],
        session: Session,
        eager: bool | None = None,
    ):
        self.model = model
        self.session = session
        self.eager = eager

    def apply_filters(self, stmt: Select, filters: dict[str, Any]) -> Select:
        pagination = {}

        order_by = filters.pop("order_by", None)
        reverse = filters.pop("reverse", False)

        page = filters.pop("page", None)

        page_size = filters.pop("page_size", None)

        for filter_parameter, value in filters.items():
            field_name, filter_type = filter_parameter.split("__")

            column = getattr(self.model, field_name)

            filter_func = FILTER_MAP[filter_type]

            stmt = stmt.where(filter_func(column, value))

        if order_by:
            order_field = getattr(self.model, order_by)
            stmt = stmt.order_by(desc(order_field) if reverse else order_field)

        if page is not None and page_size is not None:
            pagination["page"] = page
            pagination["page_size"] = page_size

            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = self.session.scalar(count_stmt)

            pagination["total"] = total
            pagination["pages"] = ceil(total / page_size) if total > 0 else 0

            stmt = stmt.limit(page_size)
            stmt = stmt.offset((page - 1) * page_size)

        return stmt, pagination

    def _get_by_id(self, id: str) -> T:
        instance = self.session.query(self.model).filter(self.model.id == id).first()

        if not instance:
            raise NotFoundException

        return instance

    def get_by_field(self, field_name: str, value) -> T:
        instance = (
            self.session.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .first()
        )

        if not instance:
            raise NotFoundException

        return self.read_schema.model_validate(instance, from_attributes=True)

    def create(self, data: dict[str, Any]):
        instance = self.model(**data)

        self.session.add(instance)
        self.session.flush()

        return instance

    def get(self, id: str) -> T:
        instance = self._get_by_id(id)

        return instance

    # TODO: implement eager loading
    def list(self, filters: dict[str, Any] = None) -> list[T] | dict[str, Any]:
        stmt = select(self.model)

        pagination = {}

        if filters:
            stmt, pagination = self.apply_filters(stmt=stmt, filters=filters)

        result = self.session.execute(stmt)

        result = result.scalars().all()

        if pagination:
            pagination["items"] = result
            return pagination

        return result

    def update(self, id: str, data: dict) -> T:
        instance = self._get_by_id(id)

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        return self.read_schema.model_validate(instance, from_attributes=True)

    def delete(self, id: str) -> None:
        instance = self._get_by_id(id)
        self.session.delete(instance)


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

    def eager_load(self, stmt: Select, eager: bool | None = None) -> Select:
        use_eager = eager if eager is not None else self.eager

        if use_eager:
            relationships = self.get_relationships()

            for rel in relationships:
                stmt = stmt.options(selectinload(getattr(self.model, rel)))

        return stmt

    async def apply_filters(self, stmt: Select, filters: dict[str, Any]) -> Select:
        pagination = {}

        order_by = filters.pop("order_by", None)
        reverse = filters.pop("reverse", False)

        page = filters.pop("page", None)
        page_size = filters.pop("page_size", None)

        for filter_parameter, value in filters.items():
            if "__" in filter_parameter:
                field_name, filter_type = filter_parameter.split("__")
            else:
                field_name = filter_parameter
                filter_type = "exact"

            column = getattr(self.model, field_name)

            filter_func = FILTER_MAP.get(filter_type, None)

            if not filter_func:
                raise ValueError(f"Invalid filtering option: {filter_type}")

            stmt = stmt.where(filter_func(column, value))

        if order_by:
            order_field = getattr(self.model, order_by)
            stmt = stmt.order_by(desc(order_field) if reverse else order_field)

        if page is not None and page_size is not None:
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = await self.session.scalar(count_stmt)
            pages = ceil(total / page_size) if total > 0 else 0

            offset = (page - 1) * page_size

            stmt = stmt.offset(offset)
            stmt = stmt.limit(page_size)

            pagination["total"] = total
            pagination["pages"] = pages

            pagination["page"] = page if page > 0 else 1
            pagination["page_size"] = page_size

        return stmt, pagination

    def get_relationships(self):
        mapper = inspect(self.model)
        return list(mapper.relationships.keys())

    async def _get_by_id(self, id: str, eager: bool | None = None) -> T:
        stmt = select(self.model).where(self.model.id == id)

        stmt = self.eager_load(stmt, eager)

        result = await self.session.execute(stmt)

        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundException

        return instance

    async def get_by_field(
        self,
        field_name: str,
        value: Any,
        eager: bool | None = None,
    ) -> T:
        stmt = select(self.model).where(getattr(self.model, field_name) == value)

        stmt = self.eager_load(stmt, eager)

        result = await self.session.execute(stmt)

        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundException

        return instance

    async def create(self, data: dict[str, Any]) -> T:
        instance = self.model(**data)

        self.session.add(instance)

        await self.session.flush()

        instance = await self._get_by_id(instance.id)

        return instance

    async def retrieve(
        self,
        id: str,
        eager: bool | None = None,
        depth: int | None = None,
    ) -> T:
        return await self._get_by_id(id, eager=eager)

    async def list(
        self, filters: dict[str, Any] = None, eager: bool | None = None
    ) -> list[T] | dict:
        stmt = select(self.model)

        stmt = self.eager_load(stmt, eager)

        pagination = {}

        if filters:
            stmt, pagination = await self.apply_filters(stmt=stmt, filters=filters)

        result = await self.session.execute(stmt)

        result = result.scalars().all()

        if pagination:
            pagination["items"] = result
            return pagination

        return result

    # TODO: optimize update operation
    async def update(
        self,
        id: str,
        data: dict[str, Any],
        eager: bool | None = None,
    ) -> T:
        instance = await self._get_by_id(id, eager=False)

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.session.flush()
        self.session.expire(instance)

        instance = await self._get_by_id(id, eager=eager)

        return instance

    async def delete(self, id: str) -> None:
        instance = await self._get_by_id(id)
        await self.session.delete(instance)
