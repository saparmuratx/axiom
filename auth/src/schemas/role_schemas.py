from typing import Any

from pydantic import BaseModel, ConfigDict

from src.schemas.schema_mixins import DBObjectMixin, UUIDMixin, UUIDTimeStampMixin


class RoleSchema(BaseModel, UUIDTimeStampMixin, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    permissions: dict[str, Any]


class RoleUpdateSchema(BaseModel, DBObjectMixin):
    title: str
    description: str
    permissions: dict[str, Any]


class RoleCreateSchema(BaseModel):
    title: str
    descriptioin: str
    permissions: dict[str, Any]


class RoleCreateResponseSchema(BaseModel, DBObjectMixin):
    title: str
    descriptioin: str
    permissions: dict[str, Any]


class RoleInlineSchema(BaseModel, UUIDMixin):
    title: str
    descriptioin: str
