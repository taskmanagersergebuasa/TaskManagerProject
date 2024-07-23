from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

class Settings(BaseSettings):
    IS_POSTGRES: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_SQLITE: str

    class Config:
        env_file = ".env"

settings = Settings()