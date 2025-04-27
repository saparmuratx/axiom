from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4

from src.schemas.schema_mixins import DBObjectMixin, UUIDTimeStampMixin


class ProfileInlineSchema(BaseModel, UUIDTimeStampMixin):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None
    last_name: str | None
    phone_number: str | None


class ProfileSchema(BaseModel, UUIDTimeStampMixin, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None
    last_name: str | None
    phone_number: str | None
    user_id: UUID4 | None


class ProfileCreateSchema(BaseModel, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    user_id: UUID4


class ProfileUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
