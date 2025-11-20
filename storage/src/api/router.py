from fastapi import APIRouter

from src.api.chapter_api import chapter_router
from src.api.chunk_api import chunk_router

storage_router = APIRouter(prefix="/storage")


storage_router.include_router(chapter_router)
storage_router.include_router(chunk_router)

