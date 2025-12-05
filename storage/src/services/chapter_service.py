from axiom.services.generic_crud_service import AsyncGenericCRUDService

from src.repository.chapter_repository import AsyncChapterRepository
from src.models.storage_models import Chapter


class ChapterCRUDService(AsyncGenericCRUDService[AsyncChapterRepository]):
    async def retrieve(self, id: str):
        chapter = await self.get(id)

        return chapter

    async def create_chapter(self, data: dict) -> Chapter:
        chapter = await super().create(data)

        return chapter
