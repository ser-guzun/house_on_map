from typing import Sequence

from sqlalchemy import Row

from src.utils.unitofwork import MySqlUnitOfWork


class StreamService:
    def __init__(self, uow: MySqlUnitOfWork):
        self.uow = uow

    async def get_all_streams(self) -> Sequence[Row]:
        async with self.uow as uow:
            streams = await uow.streams.find_all()
            await uow.commit()
            return streams
