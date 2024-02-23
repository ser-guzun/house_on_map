from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/dbname"
# engine = create_async_engine(settings.DATABASE_URL, echo=True)

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
