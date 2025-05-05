from urllib import response
from fastapi import APIRouter, Header, Response, status, HTTPException
from fastapi.requests import Request
from pydantic import UUID4

from src.repository.profile_repository import ProfileRepository
from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository
from src.repository.repository_exceptions import NotFoundException

from src.services.profile_service import ProfileService
from src.services.user_service import UserService
from src.schemas.user_schemas import UserSchema, UserUpdateSchema

from src.api.api_exceptions import make_not_found
from src.utils import debug_print
from starlette.datastructures import State


users_router = APIRouter(tags=["Users"])


@users_router.get("/users", response_model=list[UserSchema])
async def list_users(request: Request):
    data = request.state

    debug_print(request=data)

    try:
        with UnitOfWork() as unit_of_work:
            repository = UserRepository(unit_of_work.session)
            service = UserService(repository)

            users = service.list_users()

        return users

    except Exception as e:
        return Response(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@users_router.get("/users/{user_id}", response_model=UserSchema)
def retrieve_user(user_id: UUID4):
    try:
        with UnitOfWork() as unit_of_work:
            repository = UserRepository(unit_of_work.session)
            service = UserService(repository)

            user = service.get_user(str(user_id))

    except NotFoundException as e:
        raise make_not_found("User")
    except Exception as e:
        return Response(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@users_router.patch("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: UUID4, data: UserUpdateSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repository = UserRepository(unit_of_work.session)
            service = UserService(repository)

            user = service.update_user(user_id, data)
    except NotFoundException as e:
        raise make_not_found("User")
    except Exception as e:
        return Response(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user


@users_router.delete("/users/{user_id}", response_model=None)
def delete_user(user_id: str):
    try:
        with UnitOfWork() as unit_of_work:
            profile_repository = ProfileRepository(unit_of_work.session)
            user_repository = UserRepository(unit_of_work.session)

            profile_service = ProfileService(profile_repository)
            user_service = UserService(user_repository)

            profile_service.delete_user_profile(user_id)
            user_service.delete_user(user_id)

    except NotFoundException as e:
        raise make_not_found("User")

    except Exception as e:
        return Response(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@users_router.post("/users/{user_id}/deactivate")
def deactivate_user(user_id: str):
    try:
        with UnitOfWork() as unit_of_work:
            user_repository = UserRepository(unit_of_work.session)
            user_service = UserService(user_repository)

            user_service.deactivate_user(user_id)

    except NotFoundException as e:
        raise make_not_found("User")

    # return Response(status_code=)
