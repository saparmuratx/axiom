from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T", bound=BaseModel)


class PaginationSchema(BaseModel, Generic[T]):
    total: int
    pages: int
    page: int
    page_size: int
    items: list[T]
