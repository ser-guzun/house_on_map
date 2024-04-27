"""Репозитории для работы с таблицами в MySQL-БД"""
from sqlalchemy import Table, select
from sqlalchemy.orm import Session

from src.dependencies.mysql_db import get_table


class StreamsTableRepository:
    table_name = "streams"

    def __init__(self, session: Session):
        self.session: Session = session
        self.table: Table = get_table(self.table_name)

    def find_all(self):
        statement = select(self.table)
        result = self.session.execute(statement)
        res = result.all()
        return res
