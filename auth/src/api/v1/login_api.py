from datetime import datetime, timedelta
from logging import getLogger

from fastapi import status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from src.services.service_exception import (
    InvalidPasswordException,
    UserNotActiveException,
)
from src.api.api_exceptions import IncorrectOldPasswordException
from src.config import settings
from src.utils import get_jwt_service

from src.gateway.email_gateway import EmailGateway

from src.services.user_service import UserService
from src.services.login_service import LoginUserService
from src.services.password_service import PasswordService

from src.repository.repository_exceptions import NotFoundException
from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository

from src.schemas.user_schemas import UserUpdateSchema
from src.schemas.login_schemas import (
    IssueAccessTokenSchema,
    ChangePasswordSchema,
    LoginSchema,
)


login_router = APIRouter(tags=["Login"])


logger = getLogger(__name__)


@login_router.post("/login", response_model=IssueAccessTokenSchema)
def login(data: LoginSchema):
    try:
        with UnitOfWork() as unit_of_work:
            user_repository = UserRepository(session=unit_of_work.session)

            jwt_service = get_jwt_service()
            
            password_service = PasswordService()

            login_service = LoginUserService(
                user_repository=user_repository,
                jwt_service=jwt_service,
                password_service=password_service,
            )

            token, user = login_service.login(**data.model_dump())

        return IssueAccessTokenSchema(access_token=token, user_id=str(user.id))

    except UserNotActiveException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (NotFoundException, InvalidPasswordException) as e:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    except Exception as e:
        unit_of_work.rollback()

        print()

        logger.log(f"Login failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@login_router.post("/change-password")
def change_password(request: Request, data: ChangePasswordSchema):
    try:
        with UnitOfWork() as unit_of_work:
            password_service = PasswordService()

            user_repository = UserRepository(session=unit_of_work.session)

            user_id = request.state.user_id

            user = user_repository.get_db_user(user_id)

            is_old_valid = password_service.verify_password(
                data.old_password, user.password
            )

            if not is_old_valid:
                raise IncorrectOldPasswordException()

            new_password_hash = password_service.get_password_hash(data.new_password)

            user_repository.change_password(user_id, new_password=new_password_hash)

        return JSONResponse(
            content={"detail": "Password changed successfully"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        logger.info(str(e))

        print(type(e))
        print(str(e))

        unit_of_work.rollback()

        raise HTTPException(status_code=400, detail="Changing password failed")
