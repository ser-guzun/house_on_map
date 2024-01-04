import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dbname")
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    USERS_DB = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$YIz8ckQwTrbjRu5FAR9bFOjjKA4miDkaAcQoXkvpspVFqSF7pmI2K",
            "disabled": False,
        },
        "alice": {
            "username": "alice",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "hashed_password": "fakehashedsecret2",
            "disabled": True,
        },
    }
    SECRET_KEY = (
        "11d54f8d467e546e5e5bea049faa1745b8ce40dcf4cca0b8be3e14bc06cf44ac"
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings: Settings = Settings()
