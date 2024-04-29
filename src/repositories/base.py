from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.mysql_db import get_table


class SQLAlchemyTableRepository:
    table_name = None

    def __init__(self, session: AsyncSession, table_name: str):
        self.session: AsyncSession = session
        self.table: Table = get_table(table_name)

    async def find_all(self):
        statement = select(self.table)
        result = await self.session.execute(statement)
        return result.all()

    async def find_one(self, **filter_by):
        statement = select(self.table).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one()


class SQLAlchemyModelRepository:
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
