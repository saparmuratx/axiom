from contextlib import asynccontextmanager

from fastapi import FastAPI

from axiom.logging import setup_logging

from src.api.router import library_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("uvicorn")
    
    yield
    
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(library_router)
