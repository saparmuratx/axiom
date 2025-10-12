from fastapi import APIRouter


from src.api.v2.login_api import login_router


auth_router_v2 = APIRouter(prefix="/auth")

auth_router_v2.include_router(login_router)