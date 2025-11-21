from src.schemas.profile_schemas import ProfileCreateSchema, ProfileUpdateSchema
from src.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    def get_profile(self, id):
        profile = self.repository.get(id)

        return profile
    
    
    def list_profile(self):
        profile = self.repository.list()

        return profile
    


    def create_profile(self, data: ProfileCreateSchema) -> ProfileCreateSchema:
        profile = self.repository.create(data)

        return profile

    def update_profile(self, id: str, data: ProfileUpdateSchema):
        profile = self.repository.update(id, data)

        return profile

    def delete_user_profile(self, user_id: str):
        self.repository.delete_by_user_id(user_id=user_id)
