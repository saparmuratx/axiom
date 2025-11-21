from axiom.service.jwt_service import JWTService

from src.config import settings


jwt_service = JWTService(
    algorithm="HS256",
    secret_key=settings.SECRET_KEY,
)

def get_jwt_service():
    return jwt_service