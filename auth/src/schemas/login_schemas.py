from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(examples=["yourpassword"])


class AccessTokenSchema(BaseModel):
    access_token: str
