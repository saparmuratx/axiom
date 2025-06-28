from typing import Generic, TypeVar

TRepository = TypeVar("TRepository")
CreateSchema = TypeVar("CreateSchema")
ReadSchema = TypeVar("ReadSchema")
UpdateSchema = TypeVar("UpdateSchema")

class GenericCRUDService(Generic[TRepository, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(self, repository: TRepository):
        self.repository = repository

    def get(self, id: str) -> ReadSchema:
        return self.repository.get(id)

    def get_by_field(self, field_name: str, value) -> ReadSchema:
        return self.repository.get_by_field(field_name, value)

    def create(self, data: CreateSchema) -> ReadSchema:
        return self.repository.create(data)

    def update(self, id: str, data: UpdateSchema) -> ReadSchema:
        return self.repository.update(id, data)

    def delete(self, id: str):
        return self.repository.delete(id)


class AsyncGenericCRUDService(Generic[TRepository, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(self, repository: TRepository):
        self.repository = repository

    async def get(self, id: str) -> ReadSchema:
        return await self.repository.get(id)

    async def get_by_field(self, field_name: str, value) -> ReadSchema:
        return await self.repository.get_by_field(field_name, value)

    async def create(self, data: CreateSchema) -> ReadSchema:
        return await self.repository.create(data)

    async def update(self, id: str, data: UpdateSchema) -> ReadSchema:
        return await self.repository.update(id, data)

    async def delete(self, id: str):
        return await self.repository.delete(id)


