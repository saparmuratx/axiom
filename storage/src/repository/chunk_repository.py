from axiom.repository.generic_repository import (
    GenericRepository,
    AsyncGenericRepository,
)

from src.models.storage_models import Chunk
from src.schemas.chunk_schemas import (
    ChunkCreateSchema,
    ChunkUpdateSchema,
    ChunkSchema,
)


class ChunkRepository(
    GenericRepository[Chunk, ChunkCreateSchema, ChunkSchema, ChunkUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Chunk,
            session=session,
            default_schema=ChunkSchema,
            create_schema=ChunkCreateSchema,
            read_schema=ChunkSchema,
            update_schema=ChunkUpdateSchema,
        )


class AsyncChunkRepository(
    AsyncGenericRepository[Chunk, ChunkCreateSchema, ChunkSchema, ChunkUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Chunk,
            session=session,
            default_schema=ChunkSchema,
            create_schema=ChunkCreateSchema,
            read_schema=ChunkSchema,
            update_schema=ChunkUpdateSchema,
        )
