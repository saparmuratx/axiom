from pydantic import BaseModel, EmailStr, ConfigDict, UUID4, Field


from src.schemas.schema_mixins import DBObjectMixin, UUIDTimeStampMixin
from src.schemas.role_schemas import RoleSchema
from src.schemas.profile_schemas import ProfileInlineSchema


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str = Field(
        examples=["youroldpassword"],
        min_length=8,
        max_length=128,
    )


class UserCreateResponseSchema(BaseModel, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    is_active: bool | None


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
