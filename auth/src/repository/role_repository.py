from sqlalchemy.orm import Session

from src.repository.repository_exceptions import NotFoundException
from src.models.auth_models import Role
from src.schemas.role_schemas import RoleSchema, RoleUpdateSchema


class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        role = self.session.query(Role).filter(Role.id == id).first()

        if not role:
            return NotFoundException

        return role

    def get_by_title(self, title: str):
        role = self.session.query(Role).filter(Role.title == title).first()

        if not role:
            return NotFoundException

        res = RoleSchema.model_validate(role)

        return res

    def get(self, id: str) -> RoleSchema:
        role = self._get_by_id(id)

        return RoleSchema.model_validate(role)

    def update(self, id: str, data: RoleUpdateSchema):
        role = self._get_by_id(id)

        for key, value in data.to_dict().items():
            if hasattr(role, key):
                setattr(role, key, value)

        return RoleSchema.model_validate(role)

    def delete(self, id: str):
        role = self._get_by_id(id)

        self.session.delete(role)
