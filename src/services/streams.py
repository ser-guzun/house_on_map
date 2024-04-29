from typing import Sequence

from sqlalchemy import Row

from src.utils.unitofwork import MySqlUnitOfWork


class StreamService:
    @staticmethod
    async def get_all_streams(uow: MySqlUnitOfWork) -> Sequence[Row]:
        async with uow:
            streams = await uow.streams.find_all()
            await uow.commit()
            return streams
