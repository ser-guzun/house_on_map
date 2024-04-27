import pytest
import pytest_asyncio

from src.services.streams import StreamService
from src.utils.unitofwork import MySqlUnitOfWork


@pytest_asyncio.fixture
async def mysql_unit_of_work() -> MySqlUnitOfWork:
    return MySqlUnitOfWork()


@pytest.mark.asyncio
async def test_get_all_streams(mysql_unit_of_work: MySqlUnitOfWork):
    streams_db = await StreamService().get_all_streams(uow=mysql_unit_of_work)
    print(
        f"""
        {streams_db}
    """
    )
    assert streams_db
