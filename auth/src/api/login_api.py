from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from src.config import settings

from src.gateway.email_gateway import EmailGateway

from src.services.user_service import UserService
from src.services.login_service import LoginUserService
from src.services.jwt_service import JWTService

from src.services.password_service import PasswordService


from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository

from src.schemas.login_schema import AccessTokenSchema, LoginSchema


login_router = APIRouter(prefix="/auth", tags=["Login"])


@login_router.post("/login", response_model=AccessTokenSchema)
def login(data: LoginSchema):
    with UnitOfWork() as unit_of_work:
        try:
            user_repository = UserRepository(session=unit_of_work.session)

            jwt_service = JWTService(
                algorithm="RS256",
                private_key_path=settings.PRIVATE_KEY,
                public_key_path=settings.PUBLIC_KEY,
            )
            password_service = PasswordService()

            login_service = LoginUserService(
                user_repository=user_repository,
                jwt_service=jwt_service,
                password_service=password_service,
            )

            token = login_service.login(**data.model_dump())

        except Exception as e:
            unit_of_work.rollback()

            raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")

    return AccessTokenSchema(access_token=token)
