from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from axiom.schema.schema_mixins import UUIDTimeStampMixin, DBObjectMixin


class ChunkBaseSchema(BaseModel):
    size: Optional[int] = None
    content: Optional[str] = None
    prev_chunk: Optional[str] = None
    next_chunk: Optional[str] = None


class ChunkInlineSchema(DBObjectMixin, UUIDTimeStampMixin, ChunkBaseSchema):
    class Config:
        from_attributes = True


class ChunkCreateSchema(DBObjectMixin, ChunkBaseSchema):
    chapter_id: str


class ChunkUpdateSchema(DBObjectMixin, BaseModel):
    size: Optional[int] = None
    content: Optional[str] = None
    prev_chunk: Optional[str] = None
    next_chunk: Optional[str] = None


class ChunkSchema(DBObjectMixin, UUIDTimeStampMixin, ChunkBaseSchema):
    chapter_id: UUID4
