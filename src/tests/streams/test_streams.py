import pytest
import pytest_asyncio

from src.services.streams import StreamService
from src.utils.unitofwork import MySqlUnitOfWork


@pytest_asyncio.fixture
async def mysql_unit_of_work() -> MySqlUnitOfWork:
    return MySqlUnitOfWork()


@pytest_asyncio.fixture
async def stream_service(mysql_unit_of_work: MySqlUnitOfWork) -> StreamService:
    return StreamService(uow=mysql_unit_of_work)


@pytest.mark.asyncio
async def test_get_all_streams(stream_service: StreamService):
    streams_db = await stream_service.get_all_streams()
    assert streams_db[0] == (1, "stream_1", "kind_one")
    assert streams_db[1] == (2, "stream_2", "kind_two")
