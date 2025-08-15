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


def test_async_repo():
    import asyncio
    from axiom.repository.unit_of_work import AsyncUnitOfWork
    import uuid
    from datetime import date

    database_url = (
        "postgresql+asyncpg://axiom:5ECiqJSKBiKjhisyp5a5V8jJQKZXFjbO@localhost:5433/library"
    )
    
    async def main():
        async with AsyncUnitOfWork(database_url=database_url) as unit_of_work:
            repo = AsyncBookRepository(session=unit_of_work.session)

            book_data = BookCreateSchema(
                title=f"Async Test Book #{random.randint(1, 100)}",
                published_at=date(2024, 1, 1),
                edition="First",
                author_id=uuid.UUID("82312f1e-0cbe-4c9b-bf2f-f148f09506a2"),
            )

            book_id = "64ed85ad-0f99-45a8-be92-c4d0e045bf28"

            book = await repo.retrieve(id=book_id, eager=True, depth=0)
            
            from pprint import pprint
 
            print("BOOK SCHEMA MODEL DUMP")
            pprint(book.model_dump(), indent=4)
 
            book_obj = book._object

            print("\nBOOK_OBJ RELATIONSHIOPS")

            await book_obj.eager_load(depth=1)

            from sqlalchemy import inspect as sa_inspect

            mapper = sa_inspect(type(book_obj))
            relationships = mapper.relationships.keys()

            print(relationships)
            

            for rel in relationships:
                print(getattr(book_obj, rel))

    asyncio.run(main())


def test_sync_repo():
    from axiom.repository.unit_of_work import UnitOfWork
    from datetime import date

    database_url = (
        "postgresql://axiom:5ECiqJSKBiKjhisyp5a5V8jJQKZXFjbO@localhost:5433/library"
    )

    with UnitOfWork(database_url=database_url) as unit_of_work:
        repo = BookRepository(session=unit_of_work.session)

        book_data = BookCreateSchema(
            title="Test Book",
            published_at=date(2024, 1, 1),
            edition="First",
            author_id="82312f1e-0cbe-4c9b-bf2f-f148f09506a2",
        )

        book = repo.create(data=book_data)
        # book = repo.create(data=book_data)

        print("Created book:", book)
        print(f"TYPE OF BOOK: {type(book)}")

if __name__ == "__main__":
    test_async_repo()
    # test_sync_repo()