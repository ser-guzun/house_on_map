import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PG_USER: str = os.getenv("PG_USER")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD")
    PG_SERVER: str = os.getenv("PG_SERVER")
    PG_PORT: str = os.getenv("PG_PORT")
    PG_DB: str = os.getenv("PG_DB")
    PG_ECHO_DB: bool = os.getenv("PG_ECHO_DB")
    PG_DATABASE_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"

    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    MYSQL_ECHO_DB: bool = os.getenv("MYSQL_ECHO_DB")
    MYSQL_DATABASE_URL: str = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1


settings: Settings = Settings()
