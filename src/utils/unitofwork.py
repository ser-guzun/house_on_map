from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.dependencies.mysql_db import session_maker as mysql_session_maker
from src.dependencies.pg_db import async_session_maker as pg_async_session_maker
from src.repositories.mysql.repositories import StreamsTableRepository
from src.repositories.repositories import (
    HouseModelRepository,
    UserModelRepository,
)


class IUnitOfWork(ABC):
    users: Type[UserModelRepository]
    houses: Type[HouseModelRepository]

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class PgUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = pg_async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.users: UserModelRepository = UserModelRepository(
            session=self.session
        )
        self.houses: HouseModelRepository = HouseModelRepository(
            session=self.session
        )

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class MySqlUnitOfWork:
    def __init__(self):
        self.session_factory = mysql_session_maker

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.streams: StreamsTableRepository = StreamsTableRepository(
            session=self.session
        )

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
