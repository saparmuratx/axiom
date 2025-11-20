from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import UUID4

from src.services.author_service import AuthorCRUDService
from src.schemas.author_schemas import AuthorSchema, AuthorCreateSchema, AuthorUpdateSchema
from src.repository.author_repository import AsyncAuthorRepository
from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException
from src.config import settings


author_router_alt = APIRouter(prefix="/authors", tags=["Authors"])


# Dependency: Provides a ready-to-use CRUD service with a managed session
async def get_author_service() -> AsyncGenerator[AuthorCRUDService, None]:
    async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as uow:
        repo = AsyncAuthorRepository(uow.session)
        yield AuthorCRUDService(repo)
        await uow.commit()


@author_router_alt.post(
    "", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED
)
async def create_author(data: AuthorCreateSchema, service: AuthorCRUDService = Depends(get_author_service)):
    try:
        author = await service.create_author(data)
        return author
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@author_router_alt.get("", response_model=list[AuthorSchema])
async def list_authors(service: AuthorCRUDService = Depends(get_author_service)):
    try:
        authors = await service.list_authors()
        return authors
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@author_router_alt.get("/{author_id}", response_model=AuthorSchema)
async def retrieve_author(author_id: UUID4, service: AuthorCRUDService = Depends(get_author_service)):
    try:
        author = await service.get_author(str(author_id))
        return author
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@author_router_alt.patch("/{author_id}", response_model=AuthorSchema)
async def update_author(author_id: UUID4, data: AuthorUpdateSchema, service: AuthorCRUDService = Depends(get_author_service)):
    try:
        author = await service.update_author(str(author_id), data)
        return author
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@author_router_alt.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: UUID4, service: AuthorCRUDService = Depends(get_author_service)):
    try:
        await service.delete_author(str(author_id))
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Author not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
