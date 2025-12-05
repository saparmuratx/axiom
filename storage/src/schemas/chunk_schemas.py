from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from axiom.schemas import UUIDTimeStampMixin


class ChunkBaseSchema(BaseModel):
    size: Optional[int] = None
    content: Optional[str] = None
    prev_chunk: Optional[str] = None
    next_chunk: Optional[str] = None


class ChunkInlineSchema(UUIDTimeStampMixin, ChunkBaseSchema):
    class Config:
        from_attributes = True


class ChunkCreateSchema(ChunkBaseSchema):
    chapter_id: str


class ChunkUpdateSchema(BaseModel):
    size: Optional[int] = None
    content: Optional[str] = None
    prev_chunk: Optional[str] = None
    next_chunk: Optional[str] = None


class ChunkSchema(UUIDTimeStampMixin, ChunkBaseSchema):
    chapter_id: UUID4
