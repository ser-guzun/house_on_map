from typing import AsyncGenerator

from sqlalchemy import Engine, MetaData, Table, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from src.settings import settings

# асинхронный движок для асинхронных операций
async_engine: AsyncEngine = create_async_engine(
    settings.MYSQL_DATABASE_URL, echo=settings.MYSQL_ECHO_DB
)
# синхронный движок для синхронных операции metadata.reflect(bind=engine)
# подробнее о проблеме читай здесь: https://sqlalche.me/e/20/xd3s
sync_engine: Engine = create_engine(
    settings.MYSQL_DATABASE_URL, echo=settings.MYSQL_ECHO_DB
)

async_session_maker = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


def reflect_metadata():
    metadata = MetaData()
    metadata.reflect(bind=sync_engine)
    return metadata


def get_table(table_name: str) -> Table:
    metadata = reflect_metadata()
    return Table(
        name=table_name,
        metadata=metadata,
        autoload=True,
        autoload_with=sync_engine,
    )
