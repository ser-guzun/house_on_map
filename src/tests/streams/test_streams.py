import pytest
import pytest_asyncio

from src.services.streams import StreamService
from src.utils.unitofwork import MySqlUnitOfWork


@pytest.fixture
def mysql_unit_of_work() -> MySqlUnitOfWork:
    return MySqlUnitOfWork()


def test_get_all_streams(mysql_unit_of_work: MySqlUnitOfWork):
    streams_db = StreamService().get_all_streams(uow=mysql_unit_of_work)
    assert streams_db[0] == (1, "stream_1", "kind_one")
    assert streams_db[1] == (2, "stream_2", "kind_two")
