from pydantic import BaseModel, EmailStr, Field

from src.schemas.schema_mixins import UUIDMixin


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(examples=["yourpassword"])


class IssueAccessTokenSchema(BaseModel):
    user_id: str
    access_token: str


class RestorePasswordSchema(BaseModel):
    token: str
    password: str = Field(
        examples=["youroldpassword"],
        min_length=8,
        max_length=128,
    )


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(
        examples=["youroldpassword"],
        min_length=2,
        max_length=128,
    )
    new_password: str = Field(
        examples=["yournewpassword"],
        min_length=8,
        max_length=128,
    )
