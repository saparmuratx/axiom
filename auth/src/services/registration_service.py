from curses import raw
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from src.config import settings

from src.schemas.user_schemas import UserCreateSchema
from src.schemas.profile_schemas import ProfileCreateSchema

from src.repository.user_repository import UserRepository
from src.repository.role_repository import RoleRepository
from src.repository.profile_repository import ProfileRepository

from src.services.profile_service import ProfileService
from src.services.jwt_service import JWTService
from src.services.password_service import PasswordService
from src.services.service_exception import UserNotUniqueException

from src.gateway.email_gateway import EmailGateway


class RegistrationService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        password_service: PasswordService,
        profile_service: ProfileService,
        jwt_service: JWTService,
        email_gateway: EmailGateway = None,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.password_service = password_service
        self.profile_service = profile_service
        self.jwt_service = jwt_service
        self.email_gateway = email_gateway

    def register(self, data: UserCreateSchema):
        role = self.role_repository.get_by_title("user")

        raw_password = data.password

        data.password = self.password_service.get_password_hash(raw_password)

        try:
            user = self.user_repository.create(data)

            user._object.role_id = role.id
            self.user_repository.session.flush()
            user.refresh()

        except IntegrityError:
            raise UserNotUniqueException()

        self.profile_service.create_profile(
            ProfileCreateSchema(user_id=user._object.id)
        )

        now = datetime.now()

        payload = {
            "sub": str(user._object.id),
            "iss": "https://axiomae.xyz",
            "iat": now.timestamp(),
            "exp": (now + timedelta(hours=24)).timestamp(),
            "scope": "confirm-email",
        }

        if self.email_gateway:
            token = self.jwt_service.generate_token(payload=payload)

            url = f"{settings.CONFIRM_EMAIL_URL}{token}"

            print(f"CONFIRM EMAIL URL: {url}")

            self.email_gateway.send_email_confirmation(
                recipient=user._object.email, activate_url=url
            )

        return user
