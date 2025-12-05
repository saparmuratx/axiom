from pydantic import BaseModel
from typing import Optional

from axiom.schemas.schema_mixins import UUIDTimeStampMixin


class AuthorBaseSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None


class AuthorInlineSchema(UUIDTimeStampMixin, AuthorBaseSchema):
    class Config:
        from_attributes = True


class AuthorCreateSchema(AuthorBaseSchema):
    pass


class AuthorUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    pseudonym: Optional[str] = None


class AuthorSchema(UUIDTimeStampMixin, AuthorBaseSchema):
    pass
