# File: src/repository/author_repository.py
from axiom.repository.generic_repository import (
    GenericRepository,
    AsyncGenericRepository,
)

from src.models.library_models import Author
from src.schemas.author_schemas import (
    AuthorCreateSchema,
    AuthorUpdateSchema,
    AuthorSchema,
)


class AuthorRepository(
    GenericRepository[Author, AuthorCreateSchema, AuthorSchema, AuthorUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Author,
            session=session,
            default_schema=AuthorSchema,
            create_schema=AuthorCreateSchema,
            read_schema=AuthorSchema,
            update_schema=AuthorUpdateSchema,
        )


class AsyncAuthorRepository(
    AsyncGenericRepository[Author, AuthorCreateSchema, AuthorSchema, AuthorUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Author,
            session=session,
            default_schema=AuthorSchema,  # Added missing default_schema
            create_schema=AuthorCreateSchema,
            read_schema=AuthorSchema,
            update_schema=AuthorUpdateSchema,
        )
