from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.connectors.pg_connector import PgConnector


class DatabaseDep:
    def __init__(self):
        db_connector = PgConnector()
        self._session_maker = db_connector.session

    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker


database_dep = DatabaseDep()
SessionMakerDep = Annotated[
    async_sessionmaker[AsyncSession], Depends(database_dep.get_session_maker)
]
