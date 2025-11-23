from typing import Optional, List

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.types import UUID4


from axiom.schema.schema_mixins import UUIDTimeStampMixin, DBObjectMixin


class ChapterBaseSchema(BaseModel):
    title: Optional[str] = None
    number: Optional[int] = None
    prev_chapter: Optional[UUID4] = None
    next_chapter: Optional[UUID4] = None


class ChapterInlineSchema(DBObjectMixin, UUIDTimeStampMixin, ChapterBaseSchema):
    class Config:
        from_attributes = True


class ChapterInlineAltSchema(DBObjectMixin, UUIDTimeStampMixin, BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    next_chapter: UUID4 | None = None
    book_id: UUID4 | None = None
    
    class Config:
        from_attributes = True


class ChapterCreateSchema(DBObjectMixin, ChapterBaseSchema):
    book_id: UUID4


class ChapterCreateResponseSchema(UUIDTimeStampMixin, ChapterCreateSchema):
    prev: ChapterInlineAltSchema | None = None
    next: ChapterInlineAltSchema | None = None

    class Config:
        from_attributes = True
        

class ChapterUpdateSchema(DBObjectMixin, BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    next_chapter: UUID4 | None = None

    model_config = ConfigDict(exclude_unset=True)


class ChapterSchema(DBObjectMixin, UUIDTimeStampMixin, ChapterBaseSchema):
    book_id: UUID4
