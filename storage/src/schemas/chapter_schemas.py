from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4


from axiom.schemas import UUIDTimeStampMixin


class ChapterBaseSchema(BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    # next_chapter: UUID4 | None = None


class ChapterCreateSchema(ChapterBaseSchema):
    book_id: UUID4


class ChapterUpdateSchema(BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    # next_chapter: UUID4 | None = None


class ChapterInlineSchema(UUIDTimeStampMixin, BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    # next_chapter: UUID4 | None = None
    book_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class ChapterReadSchema(UUIDTimeStampMixin, ChapterBaseSchema):
    book_id: UUID4
    prev: ChapterInlineSchema | None = None
    # next: ChapterInlineSchema | None = None

    model_config = ConfigDict(from_attributes=True)
