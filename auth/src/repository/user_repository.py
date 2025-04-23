from sqlalchemy.orm import Session

from src.schemas.user_schemas import (
    UserCreateSchema,
    UserDBSchema,
    UserSchema,
    UserUpdateSchema,
    UserCreateResponseSchema,
)
from src.models.auth_models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        user = self.session.query(User).filter(User.id == id).first()

        return user

    def get_by_email(self, email: str) -> UserDBSchema:
        user = self.session.query(User).filter(User.email == email).first()

        if not user:
            return user

        return UserDBSchema.model_validate(user)

    def get(self, id) -> UserSchema:
        user = self._get_by_id(id)

        if not user:
            return user

        return UserSchema.model_validate(user)

    def list(self, limit=None, **filters) -> list[UserSchema]:
        users = self.session.query(User).filter(**filters).all()

        return [UserSchema.model_validate(user) for user in users]

    def create(self, data: dict) -> UserCreateResponseSchema:
        user = User(**data)

        self.session.add(user)

        res = UserCreateResponseSchema.model_validate(user)
        res._object = user

        return res

    def update(self, id, data: dict) -> UserSchema:
        user = self._get_by_id(id)

        if not user:
            return user

        for attr, value in data.items():
            setattr(user, attr, value)

        return UserSchema.model_validate(user)

    def delete(self, id):
        user = self._get_by_id(id)
        self.session.delete(user)
