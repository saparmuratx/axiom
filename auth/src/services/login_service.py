from src.repository.user_repository import UserRepository
from src.services.password_service import PasswordService
from src.services.jwt_service import JWTService

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

        verified = self.password_service.verify_password(password, user.password)

        if not verified:
            return False

        now = datetime.now()

        payload = {
            "iss": "https://axiomae.xyz",
            "sub": str(user.id),
            "aud": "http://localhost:8000",
            "iat": now.timestamp(),
            "exp": (now + timedelta(hours=24)).timestamp(),
            "scope": "login",
        }

        token = self.jwt_service.generate_token(payload=payload)

        return token
