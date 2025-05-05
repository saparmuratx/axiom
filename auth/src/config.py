from pydantic_settings import BaseSettings
from pydantic import HttpUrl
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str
    FRONT_URL: HttpUrl
    CONFIRM_EMAIL_URL: HttpUrl

    SITE_LOGO: HttpUrl
    SITE_NAME: str
    SITE_URL: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_SENDER: str
    SMTP_PASSWORD: str

    SECRET_KEY: str

    PRIVATE_KEY: str
    PUBLIC_KEY: str

    AUTH_ON: bool = True
    JWT_EXPIRY: int = 24


settings = Settings()
