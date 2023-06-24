import asyncio
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


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
        "cadastral_number": "10000",
        "longitude": 10.00,
        "latitude": 10.00,
    }
    created_house = await create_house(house=house)
    yield created_house
    await delete_house(house_id=created_house["id"])
