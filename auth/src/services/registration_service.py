from src.schemas.user_schemas import UserCreateSchema
from src.repository.user_repository import UserRepository


class RegistrationService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, user: UserCreateSchema):
        user = self.repository.create(user)

        return user
