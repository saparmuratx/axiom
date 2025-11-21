from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from fastapi import FastAPI

from src.admin.backend import admin
from src.api.v1.router import auth_router_v1
from src.api.v2.router import auth_router_v2

from axiom.logging import setup_logging
from src.config import settings
from src.utils.openapi import custom_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging("uvicorn")

    yield

    pass



app = FastAPI(lifespan=lifespan)

admin.mount_to(app)

app_v1 = FastAPI()
app_v1.openapi = custom_openapi

app_v2 = FastAPI()
app_v1.openapi = custom_openapi


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app_v1.include_router(auth_router_v1)
app_v2.include_router(auth_router_v2)

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)