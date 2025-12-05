import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

from axiom.schemas.schema_mixins import UUIDTimeStampMixin

if TYPE_CHECKING:
    from src.schemas.book_schemas import BookInlineSchema


class GenreBaseSchema(BaseModel):
    title: str
    description: str


class GenreInlineSchema(UUIDTimeStampMixin, GenreBaseSchema):
    pass


class GenreSchema(UUIDTimeStampMixin, GenreBaseSchema):
    # books: list["BookInlineSchema"]
    pass
