from contextlib import asynccontextmanager

from fastapi import FastAPI

from axiom.logging import setup_logging

from src.utils.db import check_db_connection
from src.api.router import storage_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("uvicorn")

    await check_db_connection()

    yield


# TODO: setup application metadata
app = FastAPI(lifespan=lifespan)

# TODO: setup swagger/openapi schemas
app.include_router(storage_router)
