from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import date

from axiom.schema.schema_mixins import UUIDTimeStampMixin, DBObjectMixin
from src.schemas.author_schemas import AuthorInlineSchema

class BookBaseSchema(BaseModel):
    title: str
    published_at: date
    edition: Optional[str] = None
    author_id: uuid.UUID

class BookCreateSchema(DBObjectMixin, BookBaseSchema):
    pass

class BookUpdateSchema(DBObjectMixin, BaseModel):
    title: Optional[str] = None
    published_at: Optional[date] = None
    edition: Optional[str] = None
    author_id: Optional[uuid.UUID] = None

class BookSchema(DBObjectMixin, UUIDTimeStampMixin, BookBaseSchema):
    # genres: List[uuid.UUID] = []
    # collections: List[uuid.UUID] = []
    # author: AuthorInlineSchema

    class Config:
        from_attributes = True
