from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

from src.schemas.mixins import DBObjectMixin, UUIDTimeStampMixin


class RoleSchema(BaseModel, UUIDTimeStampMixin, DBObjectMixin):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    # permissions: Dict[str, Any]
