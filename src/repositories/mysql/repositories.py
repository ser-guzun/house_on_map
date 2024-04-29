"""Репозитории для работы с таблицами в MySQL-БД"""
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import SQLAlchemyTableRepository


class StreamsTableRepository(SQLAlchemyTableRepository):
    table_name = "streams"

    def __init__(self, session: AsyncSession):
        super().__init__(session, self.table_name)

    async def find_all(self):
        statement = select(self.table)
        raw_data = await self.session.execute(statement)
        return raw_data.all()
