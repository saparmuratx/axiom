from typing import Literal

from fastapi import Query
from pydantic import BaseModel, Field

from axiom.filters import BaseFilter


from src.schemas.chapter_schemas import ChapterReadSchema


class ChapterFilter(BaseFilter):
    schema_class = ChapterReadSchema

    title__exact: str = Query(None, description="Case sensitive exact `title`")
    title__iexact: str = Query(None, description="Case insensitive exact `title`")
    title__icontains: str = Query(None, description="Case insensitive `title` contains")

    number__gte: int = Query(None, description="Chapter `number` **>=**")
    number__lte: int = Query(None, description="Chapter `mumber` **<=**")

    number__in: list[int] = Query([], description="`number` is one of specified values")
    number__notin: list[int] = Query(
        [], description="`number` is one of specified values"
    )

    order_by: Literal["title", "created_at", "updated_at", "number"] = Field(
        "created_at", description="Order By Field"
    )
    reverse: bool = Query(False, title="Reverse Ordering")

    page: int = Query(1, title="Page number", ge=1)
    page_size: int = Query(20, title="Page size", ge=1)
