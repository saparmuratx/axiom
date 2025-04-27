from fastapi import APIRouter

from src.api.registration_api import register_router
from src.api.users_api import users_router
from src.api.login_api import login_router
from src.api.profiles_api import profiles_router

auth_router = APIRouter(prefix="/auth")

auth_router.include_router(register_router)
auth_router.include_router(users_router)
auth_router.include_router(login_router)
auth_router.include_router(profiles_router)
