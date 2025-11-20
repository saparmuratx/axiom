from axiom.service.generic_crud_service import AsyncGenericCRUDService

from src.repository.chunk_repository import AsyncChunkRepository
from src.schemas.chunk_schemas import ChunkCreateSchema, ChunkUpdateSchema, ChunkSchema


class ChunkCRUDService(
    AsyncGenericCRUDService[AsyncChunkRepository, ChunkCreateSchema, ChunkSchema, ChunkUpdateSchema]
):
    async def list_chunks(self, chapter_id: str | None = None):
        if chapter_id:
            return await self.repository.list(filters=[self.repository.model.chapter_id == chapter_id])
        return await self.list()

    async def get_chunk(self, id: str):
        return await self.get(id)

    async def create_chunk(self, data: ChunkCreateSchema):
        return await self.create(data)

    async def update_chunk(self, id: str, data: ChunkUpdateSchema):
        return await self.update(id, data)

    async def delete_chunk(self, id: str):
        await self.delete(id)
