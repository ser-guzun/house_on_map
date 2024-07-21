from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings


class PgConnector:
    def __init__(self):
        __engine: AsyncEngine = create_async_engine(
            settings.pg_config.PG_DATABASE_URL,
            echo=settings.pg_config.PG_ECHO_DB,
        )
        self.session = async_sessionmaker(__engine)
