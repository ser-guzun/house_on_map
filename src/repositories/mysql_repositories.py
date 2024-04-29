from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.base import SQLAlchemyTableRepository


class StreamsTableRepository(SQLAlchemyTableRepository):
    table_name = "streams"

    def __init__(self, session: AsyncSession):
        super().__init__(session, self.table_name)
