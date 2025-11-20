# File: src/api/routers/chunk_router.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import UUID4

from src.services.chunk_service import ChunkCRUDService
from src.repository.chunk_repository import AsyncChunkRepository
from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException

from src.schemas.chunk_schemas import ChunkCreateSchema, ChunkUpdateSchema, ChunkSchema
from src.config import settings

from typing import AsyncGenerator


chunk_router = APIRouter(prefix="/chunks", tags=["Chunks"])


# Dependency for DI — manages session lifecycle
async def get_chunk_service() -> AsyncGenerator[ChunkCRUDService, None]:
    async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as uow:
        repo = AsyncChunkRepository(uow.session)
        yield ChunkCRUDService(repo)
        await uow.commit()


@chunk_router.post(
    "",
    response_model=ChunkCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_chunk(
    data: ChunkCreateSchema,
    service: ChunkCRUDService = Depends(get_chunk_service),
):
    try:
        chunk = await service.create_chunk(data)
        return chunk
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chunk_router.get("", response_model=list[ChunkSchema])
async def list_chunks(
    chapter_id: UUID4 | None = None,
    service: ChunkCRUDService = Depends(get_chunk_service),
):
    try:
        return await service.list_chunks(str(chapter_id)) if chapter_id else await service.list_chunks()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chunk_router.get("/{chunk_id}", response_model=ChunkSchema)
async def get_chunk(
    chunk_id: UUID4,
    service: ChunkCRUDService = Depends(get_chunk_service),
):
    try:
        chunk = await service.get_chunk(str(chunk_id))
        return chunk
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chunk not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chunk_router.patch("/{chunk_id}", response_model=ChunkSchema)
async def update_chunk(
    chunk_id: UUID4,
    data: ChunkUpdateSchema,
    service: ChunkCRUDService = Depends(get_chunk_service),
):
    try:
        chunk = await service.update_chunk(str(chunk_id), data)
        return chunk
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chunk not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chunk_router.delete("/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chunk(
    chunk_id: UUID4,
    service: ChunkCRUDService = Depends(get_chunk_service),
):
    try:
        await service.delete_chunk(str(chunk_id))
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chunk not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
