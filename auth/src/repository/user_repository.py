from sqlalchemy.orm import Session

from src.schemas.user_schemas import (
    UserCreateSchema,
    UserDBSchema,
    UserSchema,
    UserUpdateSchema,
    UserCreateResponseSchema,
)
from src.models.auth_models import User
from src.repository.repository_exceptions import NotFoundException


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        user = self.session.query(User).filter(User.id == id).first()

        if not user:
            raise NotFoundException

        return user

    def get_db_user(self, id: str):
        user = self._get_by_id(id)

        return UserDBSchema.model_validate(user)

    def get_by_email(self, email: str) -> UserDBSchema:
        user = self.session.query(User).filter(User.email == email).first()

        if not user:
            raise NotFoundException

        return UserDBSchema.model_validate(user)

    def get(self, id) -> UserSchema:
        user = self._get_by_id(id)

        return UserSchema.model_validate(user)

    def list(self, limit=None, **filters) -> list[UserSchema]:
        users = self.session.query(User).filter(**filters).all()

        return [UserSchema.model_validate(user) for user in users]

    def create(self, data: UserCreateSchema) -> UserCreateResponseSchema:
        user = User(**data.model_dump())

        self.session.add(user)

        res = UserCreateResponseSchema.model_validate(user)
        res._object = user

        return res

    def change_password(self, id: str, new_password: str):
        user = self._get_by_id(id)

        user.password = new_password

        return UserSchema.model_validate(user)

    def update(self, id, data: UserUpdateSchema) -> UserSchema:
        user = self._get_by_id(id)

        if not isinstance(data, dict):
            data = data.model_dump()

        for attr, value in data.items():
            setattr(user, attr, value)

        return UserSchema.model_validate(user)

    def delete(self, id):
        user = self._get_by_id(id)

        self.session.delete(user)
