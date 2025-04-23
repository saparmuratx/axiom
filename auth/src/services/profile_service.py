from src.schemas.profile_schemas import ProfileCreateSchema
from src.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def create_profile(self, data: dict) -> ProfileCreateSchema:
        profile = self.repository.create(data)

        return profile
