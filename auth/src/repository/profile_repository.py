from sqlalchemy.orm import Session

from src.models.auth_models import Profile
from src.schemas.profile_schemas import (
    ProfileCreateSchema,
    ProfileSchema,
    ProfileUpdateSchema,
)
from src.repository.repository_exceptions import NotFoundException


class ProfileRepository:
    def __init__(self, session: Session):
        self.session = session

    def _get_by_id(self, id: str):
        profile = self.session.query(Profile).filter(Profile.id == id).first()

        if not profile:
            raise NotFoundException

        return profile

    def get_by_user_id(self, user_id: str):
        profile = self.session.query(Profile).filter(Profile.user_id == user_id).first()

        if not profile:
            raise NotFoundException

        return ProfileSchema.model_validate(profile)

    def delete_by_user_id(self, user_id: str):
        profile = self.session.query(Profile).filter(Profile.user_id == user_id).first()

        if not profile:
            raise NotFoundException

        self.session.delete(profile)

    def get(self, id: str) -> ProfileSchema:
        profile = self._get_by_id(id)

        return ProfileSchema.model_validate(profile)

    def create(self, data: ProfileCreateSchema):
        profile = Profile(**data.model_dump())

        self.session.add(profile)

        res = ProfileCreateSchema.model_validate(profile)

        res._object = profile

        return res

    def list(self, **filters) -> list[ProfileSchema]:
        profiles = self.session.query(Profile).filter(**filters)

        return [ProfileSchema.model_validate(profile) for profile in profiles]

    def update(self, id: str, data: ProfileUpdateSchema) -> ProfileSchema:
        profile = self._get_by_id(id)

        for key, value in data.model_dump().items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        return ProfileSchema.model_validate(profile)

    def delete(self, id: str):
        profile = self._get_by_id(id)

        self.session.delete(profile)
