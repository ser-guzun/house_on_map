from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import House, User


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add_one(self, data: dict):
        statement = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def find_all(self):
        statement = select(self.model)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def find_one(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def edit_one(self, id: int, data: dict):
        statement = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(self.model)
        )
        result = await self.session.execute(statement)
        return result.scalar_one()

    async def delete(self, **filter_by):
        statement = delete(self.model).filter_by(**filter_by)
        await self.session.execute(statement)


class UserRepository(SQLAlchemyRepository):
    model = User


class HouseRepository(SQLAlchemyRepository):
    model = House
