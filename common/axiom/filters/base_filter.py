from pydantic import BaseModel
from typing import TypeVar, ClassVar

T = TypeVar("T", bound=BaseModel)


ALLOWED_FILTER_SUFFIXES: tuple["str"] = (
    "exact",
    "iexact",
    "contains",
    "icontains",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "in",
    "notin",
    "gt",
    "gte",
    "lt",
    "lte",
    "isnull",
)

PAGINATION_PARAMS: tuple["str"] = (
    "page",
    "page_size",
)

ORDERING_PARAMS: tuple["str"] = (
    "order_by",
    "reverse",
)


class FilterMetaclass(type(BaseModel)):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        if (
            name == "BaseFilter"
            or not hasattr(cls, "schema_class")
            or cls.schema_class is None
        ):
            return cls

        if not cls.schema_class:
            raise ValueError("`schema_class` was not defined")

        for filter_param in cls.model_fields:
            if filter_param in (PAGINATION_PARAMS + ORDERING_PARAMS):
                continue

            if "__" in filter_param:
                field_name, filter_name = filter_param.rsplit("__", 1)

                if filter_name not in ALLOWED_FILTER_SUFFIXES:
                    raise ValueError(f"Invalid filtering option: {filter_name}")

                if field_name not in cls.schema_class.model_fields:
                    raise ValueError(
                        f"Field `{field_name}` is not defined in {cls.schema_class.__name__}"
                    )

        return cls


class BaseFilter(BaseModel, metaclass=FilterMetaclass):
    model_config = {"extra": "forbid"}

    schema_class: ClassVar[type[BaseModel] | None] = None
