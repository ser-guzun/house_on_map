from sqlalchemy import Table, select
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
        return result.scalars().all()

    async def find_one(self, **filter_by):
        statement = select(self.table).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one()
