import logging
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import UUID4

from src.services.chapter_service import ChapterCRUDService
from src.repository.chapter_repository import AsyncChapterRepository
from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException

from src.schemas.chapter_schemas import ChapterCreateSchema, ChapterUpdateSchema, ChapterSchema, ChapterCreateResponseSchema
from src.config import settings


chapter_router = APIRouter(tags=["Chapters"])

logger = logging.getLogger(__name__)


async def get_chapter_service() -> AsyncGenerator[ChapterCRUDService, None]:
    async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
        repo = AsyncChapterRepository(unit_of_work.session)
        
        yield ChapterCRUDService(repo)

        await unit_of_work.commit()


@chapter_router.post(
    "/chapter", response_model=ChapterCreateResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_chapter(
    data: ChapterCreateSchema,
    service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        chapter = await service.create_chapter(data.model_dump())

        await service.repository.session.refresh(chapter.object)

        return chapter
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: add filtering, pagination
@chapter_router.get("/chapter", response_model=list[ChapterCreateResponseSchema])
async def list_chapters(service: ChapterCRUDService = Depends(get_chapter_service)):
    try:
        return await service.list_chapters(
            book_id="eb2c0c2f-4315-4466-980a-09a97c604813"
        )
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chapter_router.get("/chapter/{chapter_id}", response_model=ChapterSchema)
async def get_chapter(
    chapter_id: UUID4, service: ChapterCRUDService = Depends(get_chapter_service)
):
    try:
        return await service.get_chapter(str(chapter_id))
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chapter_router.patch("/chapter/{chapter_id}", response_model=ChapterSchema)
async def update_chapter(
    chapter_id: UUID4,
    data: ChapterUpdateSchema,
    service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        return await service.update_chapter(str(chapter_id), data.model_dump())
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@chapter_router.delete("/chapter/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(
    chapter_id: UUID4, service: ChapterCRUDService = Depends(get_chapter_service)
):
    try:
        await service.delete_chapter(str(chapter_id))
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
