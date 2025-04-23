from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, UUID4


from src.schemas.mixins import DBObjectMixin, UUIDTimeStampMixin
from src.schemas.role_schemas import RoleSchema
from src.schemas.profile_schemas import ProfileInlineSchema


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str


class UserCreateResponseSchema(BaseModel, UUIDTimeStampMixin, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_active: bool | None
    # password: str
    # role_id: str | None


class UserUpdateSchema(BaseModel):
    is_active: bool | None = None
    role_id: UUID4 | None = None


class UserSchema(BaseModel, UUIDTimeStampMixin):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_active: bool
    role: RoleSchema | None
    profile: ProfileInlineSchema | None


class UserDBSchema(BaseModel, UUIDTimeStampMixin):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str
    is_active: bool

    role: RoleSchema | None
    profile: ProfileInlineSchema | None


class UserInlineSchema(BaseModel, UUIDTimeStampMixin):
    email: EmailStr
    is_active: bool
    role: RoleSchema
