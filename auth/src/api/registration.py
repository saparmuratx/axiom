from fastapi import APIRouter, HTTPException

from ..schemas.profile_schemas import ProfileCreateSchema
from src.services.profile_service import ProfileService

from src.repository.profile_repository import ProfileRepository
from src.schemas.user_schemas import (
    UserCreateResponseSchema,
    UserCreateSchema,
    UserSchema,
)
from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository
from src.repository.role_repository import RoleRepository
from src.services.registration_service import RegistrationService

register_router = APIRouter(prefix="/auth", tags=["Registration"])


@register_router.post("/register")
def register(user: UserCreateSchema) -> UserSchema:
    with UnitOfWork() as unit_of_work:
        try:
            user_repository = UserRepository(session=unit_of_work.session)
            profile_repository = ProfileRepository(session=unit_of_work.session)
            role_repository = RoleRepository(session=unit_of_work.session)

            user_service = RegistrationService(
                user_repository=user_repository,
                role_repository=role_repository,
                profile_repository=profile_repository,
            )

            user = user_service.register(user)

            profile_service = ProfileService(
                repository=profile_repository,
            )

            unit_of_work.session.flush()

            profile_service.create(ProfileCreateSchema(user_id=user._object.id))

        except Exception as e:
            unit_of_work.rollback()

            print(f"Registration failed: {str(e)}")

            raise HTTPException(
                status_code=400, detail=f"Registration failed: {str(e)}"
            )

    return UserSchema.model_validate(user._object)
