from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
import uuid

from axiom.schema.schema_mixins import UUIDTimeStampMixin, DBObjectMixin

if TYPE_CHECKING:
    from src.schemas.book_schemas import BookInlineSchema


class AuthorBaseSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None


class AuthorInlineSchema(DBObjectMixin, UUIDTimeStampMixin, AuthorBaseSchema):
    class Config:
        from_attributes = True


class AuthorCreateSchema(DBObjectMixin, AuthorBaseSchema):
    pass


class AuthorUpdateSchema(DBObjectMixin, BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None


class AuthorSchema(DBObjectMixin, UUIDTimeStampMixin, AuthorBaseSchema):
    books:list[uuid.UUID] | list["BookInlineSchema"] = None

    class Config:
        from_attributes = True
