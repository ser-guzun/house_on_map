from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.mysql_db import session_maker as mysql_session_maker
from src.dependencies.pg_db import session_maker as pg_session_maker
from src.repositories.mysql_repositories import StreamsTableRepository
from src.repositories.pg_repositories import (
    HouseModelRepository,
    UserModelRepository,
)


class IUnitOfWork(ABC):
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
        self.session_factory = pg_session_maker

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


class MySqlUnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = mysql_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.streams: StreamsTableRepository = StreamsTableRepository(
            session=self.session
        )

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]] = None,
            exc_value: Optional[BaseException] = None,
            traceback: Optional[TracebackType] = None,
    ) -> None:
        if exc_value:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
