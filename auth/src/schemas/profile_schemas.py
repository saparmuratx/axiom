from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4

from src.schemas.mixins import UUIDTimeStampMixin

class ProfileInlineSchema(BaseModel, UUIDTimeStampMixin):
    first_name: str
    last_name: str
    phone_number: str


class ProfileSchema(BaseModel, UUIDTimeStampMixin):
    first_name: str
    last_name: str
    phone_number: str
    user_id: UUID4

