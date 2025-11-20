from axiom.repository.generic_repository import (
    GenericRepository,
    AsyncGenericRepository,
)

from src.models.storage_models import Chapter
from src.schemas.chapter_schemas import (
    ChapterCreateSchema,
    ChapterUpdateSchema,
    ChapterSchema,
)


class ChapterRepository(
    GenericRepository[Chapter, ChapterCreateSchema, ChapterSchema, ChapterUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Chapter,
            session=session,
            default_schema=ChapterSchema,
            create_schema=ChapterCreateSchema,
            read_schema=ChapterSchema,
            update_schema=ChapterUpdateSchema,
        )


class AsyncChapterRepository(
    AsyncGenericRepository[Chapter, ChapterCreateSchema, ChapterSchema, ChapterUpdateSchema]
):
    def __init__(self, session):
        super().__init__(
            model=Chapter,
            session=session,
            default_schema=ChapterSchema,
            create_schema=ChapterCreateSchema,
            read_schema=ChapterSchema,
            update_schema=ChapterUpdateSchema,
            eager=False
        )
