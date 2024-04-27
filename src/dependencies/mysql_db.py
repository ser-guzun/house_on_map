from typing import AsyncGenerator, Generator

from sqlalchemy import Engine, MetaData, Table, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.settings import settings

# синхронный движок для синхронных операции metadata.reflect(bind=engine)
# подробнее о проблеме читай здесь: https://sqlalche.me/e/20/xd3s
engine: Engine = create_engine(
    settings.MYSQL_DATABASE_URL, echo=settings.MYSQL_ECHO_DB
)

session_maker = sessionmaker(
    bind=engine, class_=Session, expire_on_commit=False
)

Base = declarative_base()


def get_session() -> Generator:
    with session_maker() as session:
        return session


def reflect_metadata():
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata


def get_table(table_name: str) -> Table:
    metadata = reflect_metadata()
    table = Table(
        table_name,
        metadata,
        autoload=True,
        autoload_with=engine,
    )
    return table
