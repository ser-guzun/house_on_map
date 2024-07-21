from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.pg_config.PG_DATABASE_URL, echo=settings.pg_config.PG_ECHO_DB
)
session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async with session_maker() as session:
        yield session
