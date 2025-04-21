from ast import List
from sqlalchemy.orm import Session

from src.schemas.user_schemas import UserCreateSchema, UserUpdateSchema
from src.repository.models import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    
    def _get_by_id(self, id: str):

        user = self.session.query(User).filter(User.id==id).first()

        return user
    
    def get(self, id):
        user = self._get_by_id(id)
        return UserCreateSchema.model_validate(user)
    
    def list(self, limit: int = None, **filters) -> List[UserCreateSchema]:
        users = self.session.query(User).filter(**filters).all()

        return [UserCreateSchema.model_validate(user) for user in users]
    
    def create(self, data: UserCreateSchema):
        user = User(**data.model_dump())

        return UserCreateSchema.model_validate(user)
    
    def update(self, id,  data: UserUpdateSchema):
        user = self._get_by_id(id)

        for attr, value in data.items():
            setattr(user, attr, value)

        return UserCreateSchema.model_validate(user)


    def delete(self, id):
        user = self._get_by_id(id)
        self.session.delete(user)
        