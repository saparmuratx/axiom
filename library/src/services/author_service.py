from axiom.service.generic_crud_service import AsyncGenericCRUDService

from src.repository.author_repository import AsyncAuthorRepository
from src.schemas.author_schemas import AuthorCreateSchema, AuthorSchema, AuthorUpdateSchema


class AuthorCRUDService(AsyncGenericCRUDService[AsyncAuthorRepository, AuthorCreateSchema, AuthorSchema, AuthorUpdateSchema]):
    async def list_authors(self):
        return await self.list()

    async def get_author(self, id: str):
        return await self.get(id)

    async def create_author(self, data: AuthorCreateSchema):
        return await self.create(data)

    async def update_author(self, id: str, data: AuthorUpdateSchema):
        return await self.update(id, data)

    async def delete_author(self, id: str):
        await self.delete(id)