from typing import List
from sqlalchemy.orm import Session

from src.schemas.user_schemas import (
    UserCreateSchema,
    UserSchema,
    UserUpdateSchema,
    UserCreateResponseSchema,
)
from src.models.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        user = self.session.query(User).filter(User.id == id).first()

        return user

    def get(self, id):
        user = self._get_by_id(id)
        return UserSchema.model_validate(user)

    def list(self, limit = None, **filters) -> List[UserSchema]:
        users = self.session.query(User).filter(**filters).all()

        return [UserSchema.model_validate(user) for user in users]

    def create(self, data: UserCreateSchema) -> UserCreateResponseSchema:
        user = User(**data.model_dump())

        self.session.add(user)

        res = UserCreateResponseSchema.model_validate(user)
        res._object = user

        return res

    def update(self, id, data: UserUpdateSchema):
        user = self._get_by_id(id)

        for attr, value in data.model_dump().items():
            setattr(user, attr, value)

        return UserCreateSchema.model_validate(user)

    def delete(self, id):
        user = self._get_by_id(id)
        self.session.delete(user)
