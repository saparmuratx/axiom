from ast import Dict
from typing import Any

from pydantic import BaseModel

from src.schemas.mixins import UUIDTimeStampMixin

class RoleSchema(BaseModel, UUIDTimeStampMixin):

    title: str
    description: str
    permissions: Dict[str, Any]


