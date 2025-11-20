from contextlib import asynccontextmanager

from fastapi import FastAPI

from axiom.logging import setup_logging

from src.api.router import storage_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("uvicorn")
    yield

    pass

app = FastAPI(lifespan=lifespan)

app.include_router(storage_router)