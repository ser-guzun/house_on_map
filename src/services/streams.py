from typing import Sequence

from sqlalchemy import Row

from src.utils.unitofwork import MySqlUnitOfWork


class StreamService:
    @staticmethod
    def get_all_streams(uow: MySqlUnitOfWork) -> Sequence[Row]:
        with uow:
            streams = uow.streams.find_all()
            uow.commit()
            return streams
