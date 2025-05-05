from ..config import Settings
from src.repository.user_repository import UserRepository

from src.services.password_service import PasswordService
from src.services.jwt_service import JWTService
from src.services.service_exception import UserNotActiveException

from src.config import settings


from datetime import datetime, timedelta


class LoginUserService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)

        if not user.is_active:
            raise UserNotActiveException()

        verified = self.password_service.verify_password(password, user.password)

        if not verified:
            return False

        print(user.model_dump())

        now = datetime.now()

        payload = {
            "iss": str(settings.SITE_URL),
            "sub": str(user.id),
            "aud": str(settings.SITE_URL),
            "iat": now.timestamp(),
            "exp": (now + timedelta(hours=24)).timestamp(),
            "scope": user.role.title,
        }

        token = self.jwt_service.generate_token(payload=payload)

        return token


class RestorePasswordService:
    def __init__(self, password_service: PasswordService):
        pass
