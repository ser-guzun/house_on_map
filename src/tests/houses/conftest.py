import pytest_asyncio

from src.models import House
from src.schemas.house import HouseCreate
from src.services.houses import HouseService
from src.utils.unitofwork import UnitOfWork


@pytest_asyncio.fixture
async def create_house(unit_of_work: UnitOfWork):
    async def wrapper(house: HouseCreate) -> House:
        house_db = await HouseService().create_house(
            house=house, uow=unit_of_work
        )
        assert house_db.cadastral_number == house.cadastral_number
        return house_db

    return wrapper


@pytest_asyncio.fixture
async def delete_house(unit_of_work: UnitOfWork):
    async def wrapper(house_id: int):
        return await HouseService().delete_house(
            house_id=house_id, uow=unit_of_work
        )

    return wrapper


@pytest_asyncio.fixture
async def house(create_house, delete_house):
    house = HouseCreate(
        cadastral_number="11:11:1111111:11",
        longitude=10.00,
        latitude=10.00,
    )
    created_house = await create_house(house=house)
    yield created_house
    await delete_house(house_id=created_house.id)
