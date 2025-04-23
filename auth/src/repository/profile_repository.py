from sqlalchemy.orm import Session

from src.models.auth_models import Profile
from src.schemas.profile_schemas import ProfileCreateSchema


class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        profile = self.session.query(Profile).filter(Profile.id == id).first()

        return profile

    def get(self, id: str) -> ProfileCreateSchema:
        profile = self._get_by_id(id)

        res = ProfileCreateSchema.model_validate(profile)

        res._object = res

        return res

    def create(self, data: dict):
        profile = Profile(**data)

        self.session.add(profile)

        res = ProfileCreateSchema.model_validate(profile)

        res._object = profile

        return res
