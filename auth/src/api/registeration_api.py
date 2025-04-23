from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from src.config import settings

from src.gateway.email_gateway import EmailGateway

from src.services.registration_service import RegistrationService
from src.services.user_service import UserService
from src.services.jwt_service import JWTService
from src.services.profile_service import ProfileService
from src.services.password_service import PasswordService

from src.repository.profile_repository import ProfileRepository
from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository
from src.repository.role_repository import RoleRepository

from src.schemas.profile_schemas import ProfileCreateSchema
from src.schemas.user_schemas import (
    UserCreateResponseSchema,
    UserCreateSchema,
    UserSchema,
)


register_router = APIRouter(prefix="/auth", tags=["Registration"])


@register_router.post("/register", response_model=UserCreateResponseSchema)
def register(user: UserCreateSchema):
    with UnitOfWork() as unit_of_work:
        try:
            user_repository = UserRepository(session=unit_of_work.session)
            profile_repository = ProfileRepository(session=unit_of_work.session)
            role_repository = RoleRepository(session=unit_of_work.session)

            jwt_service = JWTService(secret_key=settings.SECRET_KEY)
            profile_service = ProfileService(repository=profile_repository)

            email_gateway = EmailGateway(
                host=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                sender=settings.SMTP_SENDER,
                password=settings.SMTP_PASSWORD,
            )

            password_service = PasswordService()

            registration_service = RegistrationService(
                user_repository=user_repository,
                role_repository=role_repository,
                password_service=password_service,
                email_gateway=email_gateway,
                profile_service=profile_service,
                jwt_service=jwt_service,
            )

            user = registration_service.register(user)

        except Exception as e:
            unit_of_work.rollback()

            print(f"Registration failed: {str(e)}")

            raise HTTPException(
                status_code=400, detail=f"Registration failed: {str(e)}"
            )

    return user


@register_router.get("/confirm-email/{token}")
def confirm_email(token: str):
    with UnitOfWork() as unit_of_work:
        user_repository = UserRepository(unit_of_work.session)
        user_service = UserService(repository=user_repository)
        jwt_service = JWTService(secret_key=settings.SECRET_KEY)
        claims = jwt_service.validate_token(token)

        user = user_service.activate_user(claims["sub"])

    return {"detail": "Activated successfully", "claims": claims}
