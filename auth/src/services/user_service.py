from src.models.auth_models import User

from sqlalchemy.orm import Session

from src.repository.user_repository import UserRepository
from src.schemas.user_schemas import UserSchema, UserUpdateSchema


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self, **filters):
        users = self.repository.list(**filters)

        return users

    def get_user(self, id: str):
        user = self.repository.get(id)

        return user

    def update_user(self, id: str, data: UserUpdateSchema):
        user = self.repository.update(id, data=data.model_dump())

        return user

    def delete_user(self, id: str):
        self.repository.delete(id)

    def activate_user(self, id: str):
        user = self.repository.update(id, {"is_active": True})

        return user

    def deactivate_user(self, id: str):
        user = self.repository.update(id, {"is_active": False})

        return user
