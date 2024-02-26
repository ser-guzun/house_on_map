import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def create_house(client: AsyncClient):
    async def wrapper(house: dict):
        response = await client.post("/houses/", json=house)
        assert response.status_code == 200
        data = response.json()
        assert data["cadastral_number"] == house["cadastral_number"]
        return data

    return wrapper


@pytest_asyncio.fixture
async def delete_house(client: AsyncClient):
    async def wrapper(house_id: int):
        response = await client.delete(f"/houses/{house_id}")
        assert response.status_code == 200

    return wrapper


@pytest_asyncio.fixture
async def house(create_house, delete_house):
    house = {
        "cadastral_number": "11:11:1111111:11",
        "longitude": 10.00,
        "latitude": 10.00,
    }
    created_house = await create_house(house=house)
    yield created_house
    await delete_house(house_id=created_house["id"])
