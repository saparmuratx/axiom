import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

from axiom.schema.schema_mixins import DBObjectMixin, UUIDTimeStampMixin

if TYPE_CHECKING:
    from src.schemas.book_schemas import BookInlineSchema


class GenreBaseSchema(BaseModel):
    title: str
    description: str


class GenreInlineSchema(DBObjectMixin, UUIDTimeStampMixin, GenreBaseSchema):
    pass


class GenreSchema(DBObjectMixin, UUIDTimeStampMixin, GenreBaseSchema):
    # books: list["BookInlineSchema"]
    pass


