import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class AlembicConfig(BaseSettings):
    ALEMBIC_USER: str = "user"
    ALEMBIC_PASSWORD: str = "pass"
    ALEMBIC_SERVER: str = "db"
    ALEMBIC_PORT: str = 5432
    ALEMBIC_DB: str = "dbname"
    ALEMBIC_URL: str = f"postgresql+asyncpg://{ALEMBIC_USER}:{ALEMBIC_PASSWORD}@{ALEMBIC_SERVER}:{ALEMBIC_PORT}/{ALEMBIC_DB}"


class PgCongig(BaseSettings):
    PG_USER: str = "user"
    PG_PASSWORD: str = "pass"
    PG_SERVER: str = "db"
    PG_PORT: str = 5432
    PG_DB: str = "dbname"
    PG_ECHO_DB: bool = True
    PG_DATABASE_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_SERVER}:{PG_PORT}/{PG_DB}"


class Settings(BaseSettings):
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    MYSQL_ECHO_DB: bool = os.getenv("MYSQL_ECHO_DB")
    MYSQL_SYNC_DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    MYSQL_ASYNC_DATABASE_URL: str = f"mysql+asyncmy://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1

    alembic_config: AlembicConfig = AlembicConfig()
    pg_config: PgCongig = PgCongig()


settings: Settings = Settings()
