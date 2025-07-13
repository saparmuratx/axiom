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

            # book = await repo.create(data=book_data)
            book = await repo.retrieve(id=book_id, eager=False)
            
            from pprint import pprint
            
            # data = await book._object.to_dict(session=unit_of_work.session)
            # data = await book._object.to_dict()

            # pprint(book.model_dump(), indent=4)
            # pprint((book.model_dump()))
            # pprint(book.model_dump(), indent=4)

            # print(type(book._object.author))

            book_obj = book._object

            await book_obj.eager_load(unit_of_work.session)

            awaitable_attrs = book._object.awaitable_attrs
            awaitable_attrs_dict = await awaitable_attrs.__dict__

            pprint(awaitable_attrs_dict, indent=4)

            # genres = await awaitable_attrs_dict.genres

            print("c36d83b2-f1d1-4034-a25c-02d3ce439967" in book_obj.genres)
            
            author = await book._object.awaitable_attrs.author

            pprint(await book_obj.to_dict(), indent=4)

            print(f"TYPE OF BOOK: {type(book)}")
            
            # pprint(await book._object.author.to_dict(), indent=4)

            # book._object.genres.append()


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