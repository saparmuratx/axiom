from fastapi import APIRouter, Header, Response, status, HTTPException
from pydantic import UUID4

from src.repository.unit_of_work import UnitOfWork
from src.services.user_service import UserService
from src.repository.user_repository import UserRepository
from src.schemas.user_schemas import UserSchema, UserUpdateSchema


users_router = APIRouter(prefix="/auth", tags=["Users"])


@users_router.get("/users", response_model=list[UserSchema])
def list():
    try:
        with UnitOfWork() as unit_of_work:
            repository = UserRepository(unit_of_work.session)
            service = UserService(repository)

            users = service.list_users()

        return users

    except Exception as e:
        print(e)
        return Response(
            {"detail": "Something went wrong"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@users_router.get("/users/{user_id}", response_model=UserSchema)
def retrieve(user_id: UUID4):
    # try:
    with UnitOfWork() as unit_of_work:
        repository = UserRepository(unit_of_work.session)
        service = UserService(repository)

        user = service.get_user(str(user_id))

    if not user:
        raise HTTPException(
            detail="User not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user


@users_router.patch("/users/{user_id}", response_model=UserSchema)
def update(user_id: UUID4, data: UserUpdateSchema):
    with UnitOfWork() as unit_of_work:
        repository = UserRepository(unit_of_work.session)
        service = UserService(repository)

        user = service.update_user(user_id, data)

    if not user:
        raise HTTPException(
            detail={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user
