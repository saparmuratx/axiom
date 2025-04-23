from sqlalchemy.orm import Session

from src.models.models import Role
from src.schemas.role_schemas import RoleSchema


class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        role = self.session.query(Role).filter(Role.id == id).first()

        return role

    def get_by_title(self, title: str):
        role = self.session.query(Role).filter(Role.title == title).first()

        if not role:
            return None

        res = RoleSchema.model_validate(role)

        res._object = role

        return res

    def get(self, id: str) -> RoleSchema:
        role = self._get_by_id(id)

        res = RoleSchema.model_validate(role)

        res._object = role

        return res
