from fastapi import APIRouter

from src.api.registeration_api import register_router
from src.api.users_api import users_router
from src.api.login_api import login_router

auth_router = APIRouter()

auth_router.include_router(register_router)
auth_router.include_router(users_router)
auth_router.include_router(login_router)
