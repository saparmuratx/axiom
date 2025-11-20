from typing import Optional, List

from pydantic import BaseModel, ConfigDict
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


class ChapterCreateSchema(DBObjectMixin, ChapterBaseSchema):
    book_id: str


class ChapterUpdateSchema(DBObjectMixin, BaseModel):
    title: str | None = None
    number: int | None = None
    prev_chapter: UUID4 | None = None
    next_chapter: UUID4 | None = None

    model_config = ConfigDict(exclude_unset=True)

    def model_dump(self, *, mode = 'python', include = None, exclude = None, context = None, by_alias = None, exclude_unset = True, exclude_defaults = False, exclude_none = False, exclude_computed_fields = False, round_trip = False, warnings = True, fallback = None, serialize_as_any = False):
        return super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, exclude_computed_fields=exclude_computed_fields, round_trip=round_trip, warnings=warnings, fallback=fallback, serialize_as_any=serialize_as_any)
    

class ChapterSchema(DBObjectMixin, UUIDTimeStampMixin, ChapterBaseSchema):
    book_id: UUID4
