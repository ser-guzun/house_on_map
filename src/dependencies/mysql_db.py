from typing import AsyncGenerator

from sqlalchemy import Engine, MetaData, Table, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.settings import settings

# асинхронный движок для асинхронных операций
async_engine: AsyncEngine = create_async_engine(
    settings.MYSQL_ASYNC_DATABASE_URL, echo=settings.MYSQL_ECHO_DB
)

# синхронный движок для синхронной операции metadata.reflect(bind=engine),
# которая не поддерживается в AsyncEngine
# подробнее о проблеме читай здесь: https://sqlalche.me/e/20/xd3s
sync_engine: Engine = create_engine(
    settings.MYSQL_SYNC_DATABASE_URL, echo=settings.MYSQL_ECHO_DB
)

session_maker = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator:
    with session_maker() as session:
        yield session


def reflect_metadata() -> MetaData:
    metadata = MetaData()
    metadata.reflect(bind=sync_engine)
    return metadata


def get_table(table_name: str) -> Table:
    metadata = reflect_metadata()
    return Table(
        table_name,
        metadata,
        autoload=True,
        autoload_with=sync_engine,
    )
