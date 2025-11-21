import random
from axiom.repository.generic_repository import AsyncGenericRepository, GenericRepository

from src.models.library_models import Book
from src.schemas.book_schemas import BookCreateSchema, BookUpdateSchema, BookSchema


class BookRepository(
    GenericRepository[Book, BookCreateSchema, BookSchema, BookUpdateSchema,]
):
    def __init__(self, session):
        super().__init__(
            model=Book,
            session=session,
            default_schema=BookSchema,
            create_schema=BookCreateSchema,
            read_schema=BookSchema,
            update_schema=BookUpdateSchema,
        )


class AsyncBookRepository(
    AsyncGenericRepository[Book, BookCreateSchema, BookSchema, BookUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Book,
            session=session,
            default_schema=BookSchema,
            create_schema=BookCreateSchema,
            read_schema=BookSchema,
            update_schema=BookUpdateSchema,
        )
