from fastapi import APIRouter

from src.api.v1.registration_api import register_router
from src.api.v1.users_api import users_router
from src.api.v1.login_api import login_router
from src.api.v1.profiles_api import profiles_router


auth_router_v1 = APIRouter(prefix="/auth")

auth_router_v1.include_router(register_router)
auth_router_v1.include_router(users_router)
auth_router_v1.include_router(login_router)
auth_router_v1.include_router(profiles_router)

