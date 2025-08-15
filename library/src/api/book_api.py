# File: src/api/book_api.py
from fastapi import APIRouter, HTTPException, status, Request

from pydantic import UUID4

from src.repository.book_repository import AsyncBookRepository
from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException

from src.services.book_service import BookCRUDService
from src.schemas.book_schemas import BookSchema, BookUpdateSchema, BookCreateSchema

from src.utils.debug_print import debug_print

from src.config import settings

book_router = APIRouter(tags=["Books"])

BookSchema.model_rebuild()

@book_router.post("/book", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_book(data: BookCreateSchema):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncBookRepository(unit_of_work.session)
            service = BookCRUDService(repository)

            book = await service.create_book(data)
            
            await unit_of_work.commit()

            await book.object.eager_load(unit_of_work.session)

        return BookSchema.model_validate(book.object, from_attributes=True)

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@book_router.get("/book", response_model=list[BookSchema])
async def list_books(request: Request):
    data = request.state
    debug_print(state=data)

    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncBookRepository(unit_of_work.session)
            service = BookCRUDService(repository)

            books = await service.list_books()

        return books

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@book_router.get("/book/{book_id}", response_model=BookSchema)
async def retrieve_book(book_id: UUID4):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncBookRepository(unit_of_work.session)
            service = BookCRUDService(repository)

            book = await service.get_book(str(book_id))

        return book

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@book_router.patch("/book/{book_id}", response_model=BookSchema)
async def update_book(book_id: UUID4, data: BookUpdateSchema):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncBookRepository(unit_of_work.session)
            service = BookCRUDService(repository)

            book = await service.update_book(str(book_id), data)

        return book

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@book_router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID4):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncBookRepository(unit_of_work.session)
            service = BookCRUDService(repository)

            await service.delete_book(str(book_id))

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )