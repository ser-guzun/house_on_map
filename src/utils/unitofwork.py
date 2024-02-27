from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import async_session_maker
from src.repositories.repositories import HouseRepository, UserRepository


class IUnitOfWork(ABC):
    users: Type[UserRepository]
    houses: Type[HouseRepository]

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.users: UserRepository = UserRepository(session=self.session)
        self.houses: HouseRepository = HouseRepository(session=self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
