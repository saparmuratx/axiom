from fastapi import FastAPI

from src.api.router import library_router

app = FastAPI()

app.include_router(library_router)
