from logging import getLogger

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException


from axiom.repository.unit_of_work import AsyncUnitOfWork
from axiom.service.jwt_service import JWTService
from axiom.repository.exceptions import NotFoundException

from src.services.password_service import PasswordService
from src.services.login_service import AsyncLoginUserService

from src.schemas.login_schemas import IssueAccessTokenSchema, LoginSchema
from src.repository.user_repository import AsyncUserRepository
from src.config import settings

from src.services.service_exception import (
    InvalidPasswordException,
    UserNotActiveException,
)

logger = getLogger(__name__)

login_router = APIRouter(tags=["Login v2"])


@login_router.post("/login", response_model=IssueAccessTokenSchema)
async def login(request: Request, data: LoginSchema):
    try:
        async with AsyncUnitOfWork(database_url=settings.DATABASE_ASYNC_URL) as unit_of_work:
            repository = AsyncUserRepository(unit_of_work.session)

            jwt_service = JWTService(
                algorithm="RS256",
                private_key_path=settings.PRIVATE_KEY,
                public_key_path=settings.PRIVATE_KEY,
            )

            password_service = PasswordService()

            login_service = AsyncLoginUserService(
                user_repository=repository,
                password_service=password_service,
                jwt_service=jwt_service
            )

            token, user = await login_service.login(**data.model_dump())

        logger.info(f"User login for [{str(user.id)}]") 

        request.scope["session"]["user_id"] = str(user.id)
        return IssueAccessTokenSchema(access_token=token, user_id=str(user.id))

    except UserNotActiveException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (NotFoundException, InvalidPasswordException) as e:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    except Exception as e:

        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
