from sqlalchemy import select

from axiom.repository import AsyncUnitOfWork

from src.config import settings


async def check_db_connection():
    async with AsyncUnitOfWork(settings.DATABASE_URL) as unit_of_work:
        try:
            await unit_of_work.session.execute(select(1))
        except ConnectionRefusedError as e:
            print(type(e))
            raise RuntimeError("Connection to Database Failed")
