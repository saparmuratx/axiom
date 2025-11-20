from axiom.service.generic_crud_service import AsyncGenericCRUDService

from src.repository.book_repository import AsyncBookRepository
from src.schemas.book_schemas import BookCreateSchema, BookSchema, BookUpdateSchema


class BookCRUDService(AsyncGenericCRUDService[AsyncBookRepository, BookCreateSchema, BookSchema, BookUpdateSchema]):
    async def list_books(self):
        return await self.list()

    async def get_book(self, id: str):
        return await self.get(id)

    async def create_book(self, data: BookCreateSchema):
        return await self.create(data)

    async def update_book(self, id: str, data: BookUpdateSchema):
        return await self.update(id, data)

    async def delete_book(self, id: str):
        await self.delete(id)   