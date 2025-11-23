from axiom.repository.generic_repository import (
    GenericRepository,
    AsyncGenericRepository,
)

from src.models.storage_models import Chapter

class ChapterRepository(
    GenericRepository[Chapter]
):
    def __init__(self, session):
        super().__init__(
            model=Chapter,
            session=session,
        )


class AsyncChapterRepository(
    AsyncGenericRepository[Chapter]
):
    def __init__(self, session):
        super().__init__(
            model=Chapter,
            session=session,
            eager=True
        )
