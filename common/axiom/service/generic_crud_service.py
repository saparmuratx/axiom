from typing import Generic, TypeVar, Any
from axiom.repository import AsyncGenericRepository, GenericRepository


TRepository = TypeVar("TRepository", bound=GenericRepository)
TAsyncRepository = TypeVar("TAsyncRepository", bound=AsyncGenericRepository)


class GenericCRUDService(Generic[TRepository]):
    def __init__(self, repository: TRepository):
        self.repository = repository

    def create(self, data: dict[str, Any]):
        return self.repository.create(data)

    def retrieve(self, id: str):
        return self.repository.get(id)

    def get_by_field(self, field_name: str, value):
        return self.repository.get_by_field(field_name, value)

    def list(self, filters: dict[str, Any]) -> list | dict:
        return self.repository.list(filters=filters)

    def update(self, id: str, data: dict[str, Any]):
        return self.repository.update(id, data)

    def delete(self, id: str):
        return self.repository.delete(id)


class AsyncGenericCRUDService(Generic[TAsyncRepository]):
    def __init__(self, repository: TAsyncRepository):
        self.repository = repository

    async def create(self, data: dict[str, Any]):
        return await self.repository.create(data)

    async def retrieve(self, id: str):
        return await self.repository.retrieve(id)

    async def get_by_field(self, field_name: str, value):
        return await self.repository.get_by_field(field_name, value)

    async def list(self, filters: dict[str, Any] | None = None) -> list | dict:
        return await self.repository.list(filters=filters)

    async def update(self, id: str, data: dict[str, Any]):
        return await self.repository.update(id, data)

    async def delete(self, id: str):
        return await self.repository.delete(id)
