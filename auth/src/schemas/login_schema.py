from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
