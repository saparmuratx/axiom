from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI

from src.admin.backend import admin
from src.middleware.auth_middleware import JWTAuthorizationMiddleware
from src.api.router import auth_router
from src.utils.logging import setup_logging
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize logging
    setup_logging()
    yield
    # Shutdown: Optional cleanup (e.g., close database connections)
    pass


app = FastAPI()

admin.mount_to(app)

app.add_middleware(JWTAuthorizationMiddleware, aud=settings.SITE_URL)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth_router)
