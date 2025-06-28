from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase):
    pass


class AsyncBase(AsyncAttrs, DeclarativeBase):
    pass
