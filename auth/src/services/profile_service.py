from src.schemas.profile_schemas import ProfileCreateSchema
from src.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def create(self, data: ProfileCreateSchema) -> ProfileCreateSchema:
        profile = self.repository.create(data.model_dump())

        return profile
