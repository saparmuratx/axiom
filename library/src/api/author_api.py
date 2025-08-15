# File: src/api/author_api.py
from fastapi import APIRouter, HTTPException, status, Request

from pydantic import UUID4

from src.repository.author_repository import AsyncAuthorRepository
from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException

from src.services.author_service import AuthorCRUDService
from src.schemas.author_schemas import AuthorSchema, AuthorUpdateSchema, AuthorCreateSchema

from src.utils.debug_print import debug_print

from src.config import settings

author_router = APIRouter(tags=["Authors"])

AuthorSchema.model_rebuild()

@author_router.post("/author", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
async def create_author(data: AuthorCreateSchema):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncAuthorRepository(unit_of_work.session)
            service = AuthorCRUDService(repository)

            author = await service.create_author(data)
            await unit_of_work.commit()

            await author.object.eager_load(unit_of_work.session)

            print(author.object)

            print(author)

        return AuthorSchema.model_validate(author.object, from_attributes=True)

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@author_router.get("/author", response_model=list[AuthorSchema])
async def list_authors(request: Request):
    data = request.state
    debug_print(state=data)

    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncAuthorRepository(unit_of_work.session)
            service = AuthorCRUDService(repository)

            authors = await service.list_authors()

        return authors

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@author_router.get("/author/{author_id}", response_model=AuthorSchema)
async def retrieve_author(author_id: UUID4):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncAuthorRepository(unit_of_work.session)
            service = AuthorCRUDService(repository)

            author = await service.get_author(str(author_id))

        return author

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@author_router.patch("/author/{author_id}", response_model=AuthorSchema)
async def update_author(author_id: UUID4, data: AuthorUpdateSchema):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncAuthorRepository(unit_of_work.session)
            service = AuthorCRUDService(repository)

            author = await service.update_author(str(author_id), data)

        return author

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@author_router.delete("/author/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID4):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
            repository = AsyncAuthorRepository(unit_of_work.session)
            service = AuthorCRUDService(repository)

            await service.delete_author(str(author_id))

    except NotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    except Exception as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )