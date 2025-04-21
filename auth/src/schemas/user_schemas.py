from xmlrpc.client import Boolean, boolean
from pydantic import BaseModel, EmailStr, ConfigDict

from src.schemas.mixins import UUIDTimeStampMixin
from src.schemas.role_shchemas import RoleSchema
from src.schemas.profile_schemas import ProfileInlineSchema


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str


class UserCreateResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str
    is_active: boolean
    role_id: str


class UserUpdateSchema(BaseModel):
    is_active: Boolean
    role_id: str


class UserSchema(UUIDTimeStampMixin):
    email: EmailStr
    is_active: boolean
    role: RoleSchema
    profile: ProfileInlineSchema


class UserInlineSchema(UUIDTimeStampMixin):
    email: EmailStr
    is_active: boolean
    role: RoleSchema

