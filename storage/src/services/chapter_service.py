from axiom.service.generic_crud_service import AsyncGenericCRUDService

from src.repository.chapter_repository import AsyncChapterRepository
from src.schemas.chapter_schemas import ChapterCreateSchema, ChapterUpdateSchema, ChapterSchema


class ChapterCRUDService(
    AsyncGenericCRUDService[AsyncChapterRepository, ChapterCreateSchema, ChapterSchema, ChapterUpdateSchema]
):
    async def list_chapters(self, book_id: str | None = None):
        if book_id:
            return await self.repository.list(filters={"book_id": book_id}, eager=True)
        return await self.repository.list(eager=True)

    async def get_chapter(self, id: str):
        return await self.get(id)

    async def create_chapter(self, data: ChapterCreateSchema) -> ChapterCreateSchema:
        chapter = await self.create(data)

        await chapter.eager_load(self.repository.session)

        return chapter
    

    async def update_chapter(self, id: str, data: ChapterUpdateSchema):
        return await self.update(id, data)

    async def delete_chapter(self, id: str):
        await self.delete(id)
