from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class UnitOfWork:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)
        self.session = None

    def __enter__(self):
        self.session = Session(self.engine)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        try:
            if exc_type:
                self.rollback()
            else:
                self.commit()
        finally:
            if self.session:
                self.session.close()

    def rollback(self):
        if self.session:
            self.session.rollback()

    def commit(self):
        if self.session:
            self.session.commit()


class AsyncUnitOfWork:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(self.database_url)
        self.session = None

    async def __aenter__(self):
        self.session = AsyncSession(self.engine, expire_on_commit=False)
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self.session:
                await self.session.close()

    async def rollback(self):
        if self.session:
            await self.session.rollback()

    async def commit(self):
        if self.session:
            await self.session.commit()
