from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import date

from axiom.schemas.schema_mixins import UUIDTimeStampMixin

from src.schemas.genre_schemas import GenreInlineSchema
from src.schemas.author_schemas import AuthorInlineSchema


class BookBaseSchema(BaseModel):
    title: str
    published_at: date
    edition: Optional[str] = None
    author_id: uuid.UUID


class BookInlineSchema(UUIDTimeStampMixin, BookBaseSchema):
    class Config:
        from_attributes = True


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    published_at: Optional[date] = None
    edition: Optional[str] = None
    author_id: Optional[uuid.UUID] = None


class BookSchema(UUIDTimeStampMixin, BookBaseSchema):
    genres: list[GenreInlineSchema] = None
    collections: List[uuid.UUID] = None
    author: AuthorInlineSchema = None

    author_id: uuid.UUID

    class Config:
        from_attributes = True
