from profile import Profile
from src.schemas.user_schemas import UserCreateSchema, UserSchema

from src.repository.user_repository import UserRepository
from src.repository.role_repository import RoleRepository
from src.repository.profile_repository import ProfileRepository


class RegistrationService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        profile_repository: ProfileRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def register(self, data: UserCreateSchema):
        role = self.role_repository.get_by_title("user")

        user = self.user_repository.create(data)

        user._object.role = role._object

        return user
