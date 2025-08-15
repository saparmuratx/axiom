from fastapi import APIRouter

from src.api.author_api import author_router
from src.api.book_api import book_router

library_router = APIRouter(prefix="/library")


library_router.include_router(author_router)
library_router.include_router(book_router)

