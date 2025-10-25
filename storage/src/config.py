from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    CASSANDRA_URL: str
    CASSANDRA_HOST: str = "localhost"
    CASSANDRA_KEYSPACE: str
    CASSANDRA_USER: str
    CASSANDRA_PASSWORD: str
    
    DATABASE_URL: str

    DEBUG: bool = True


settings = Settings()
