from pydantic_settings import BaseSettings
from pydantic import HttpUrl
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str
    FRONT_URL: HttpUrl

    SITE_LOGO: HttpUrl 
    SITE_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_SENDER: str
    SMTP_PASSWORD: str


settings = Settings()
