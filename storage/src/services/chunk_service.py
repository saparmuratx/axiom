from axiom.services import AsyncGenericCRUDService

from src.repository.chunk_repository import AsyncChunkRepository


# TODO: update code to work with new version of axiom
class ChunkCRUDService(AsyncGenericCRUDService[AsyncChunkRepository]):
    async def list_chunks(self, chapter_id: str | None = None):
        if chapter_id:
            return await self.repository.list(
                filters=[self.repository.model.chapter_id == chapter_id]
            )
        return await self.list()

    async def get_chunk(self, id: str):
        return await self.get(id)

    async def create_chunk(self, data: dict):
        return await self.create(data)

    async def update_chunk(self, id: str, data: dict):
        return await self.update(id, data)

    async def delete_chunk(self, id: str):
        await self.delete(id)
