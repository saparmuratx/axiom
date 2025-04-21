from fastapi import APIRouter

from src.schemas.user_schemas import UserCreateResponseSchema, UserCreateSchema
from src.repository.unit_of_work import UnitOfWork
from src.repository.user_repository import UserRepository
from src.services.registration_service import RegistrationService

register_router = APIRouter(prefix="/auth", tags=["Registration"])


@register_router.post("/register")
def register(user: UserCreateSchema) -> UserCreateResponseSchema:
    with UnitOfWork() as unit_of_work:
        repository = UserRepository(session=unit_of_work.session)
        service = RegistrationService(repository=repository)

        user = service.register(user)

    return user
