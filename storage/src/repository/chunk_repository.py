from axiom.repository.generic_repository import (
    GenericRepository,
    AsyncGenericRepository,
)

from src.models.storage_models import Chunk


class ChunkRepository(
    GenericRepository[Chunk]
):
    def __init__(self, session):
        super().__init__(
            model=Chunk,
            session=session,
        )


class AsyncChunkRepository(
    AsyncGenericRepository[Chunk]
):
    def __init__(self, session):
        super().__init__(
            model=Chunk,
            session=session,
        )
