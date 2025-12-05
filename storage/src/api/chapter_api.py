import logging
from typing import AsyncGenerator, Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import UUID4

from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.repository.exceptions import NotFoundException
from axiom.filters import PaginationSchema

from src.config import settings
from src.services.chapter_service import ChapterCRUDService
from src.repository.chapter_repository import AsyncChapterRepository

from src.schemas.chapter_schemas import (
    ChapterCreateSchema,
    ChapterUpdateSchema,
    ChapterReadSchema,
)
from src.api.filters import ChapterFilter

chapter_router = APIRouter(tags=["Chapters"])

logger = logging.getLogger(__name__)


async def get_chapter_service() -> AsyncGenerator[ChapterCRUDService, None]:
    async with AsyncUnitOfWork(database_url=settings.DATABASE_URL) as unit_of_work:
        repo = AsyncChapterRepository(unit_of_work.session)

        yield ChapterCRUDService(repo)

        await unit_of_work.commit()


@chapter_router.post(
    "/chapter",
    response_model=ChapterReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_chapter(
    data: ChapterCreateSchema,
    chapter_service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        chapter = await chapter_service.create(data.model_dump())

        return chapter
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )


@chapter_router.get(
    "/chapter",
    response_model=PaginationSchema[ChapterReadSchema],
)
async def list_chapters(
    filters: Annotated[ChapterFilter, Query()],
    chapter_service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        filters = filters.model_dump(exclude_unset=True)

        chapters = await chapter_service.list(filters=filters)

        return chapters

    except Exception as e:
        logger.error(e)

        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )


@chapter_router.get("/chapter/{chapter_id}", response_model=ChapterReadSchema)
async def get_chapter(
    chapter_id: UUID4,
    chapter_service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        chapter = await chapter_service.retrieve(str(chapter_id))

        return chapter
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )


@chapter_router.patch("/chapter/{chapter_id}", response_model=ChapterReadSchema)
async def update_chapter(
    chapter_id: UUID4,
    data: ChapterUpdateSchema,
    chapter_service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        return await chapter_service.update(
            str(chapter_id),
            data.model_dump(exclude_unset=True),
        )
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )


@chapter_router.delete("/chapter/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(
    chapter_id: UUID4,
    chapter_service: ChapterCRUDService = Depends(get_chapter_service),
):
    try:
        await chapter_service.delete(str(chapter_id))
    except NotFoundException:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        )
