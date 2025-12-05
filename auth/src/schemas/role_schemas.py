from typing import Any

from pydantic import BaseModel, ConfigDict

from src.schemas.schema_mixins import UUIDMixin, UUIDTimeStampMixin


class RoleSchema(BaseModel, UUIDTimeStampMixin):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    permissions: dict[str, Any]


class RoleUpdateSchema(BaseModel):
    title: str
    description: str
    permissions: dict[str, Any]


class RoleCreateSchema(BaseModel):
    title: str
    descriptioin: str
    permissions: dict[str, Any]


class RoleCreateResponseSchema(BaseModel):
    title: str
    descriptioin: str
    permissions: dict[str, Any]


class RoleInlineSchema(BaseModel, UUIDMixin):
    title: str
    descriptioin: str
