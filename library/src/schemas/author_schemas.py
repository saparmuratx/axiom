from pydantic import BaseModel
from typing import Optional, List
import uuid

from axiom.schema.schema_mixins import UUIDTimeStampMixin, DBObjectMixin

class AuthorBaseSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None

class AuthorCreateSchema(DBObjectMixin, AuthorBaseSchema):
    pass

class AuthorUpdateSchema(DBObjectMixin, BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None

class AuthorSchema(DBObjectMixin, UUIDTimeStampMixin, AuthorBaseSchema):
    books: List[uuid.UUID] = []

    class Config:
        from_attributes = True

class AuthorInlineSchema(DBObjectMixin, UUIDTimeStampMixin, AuthorBaseSchema):
    class Config:
        from_attributes = True