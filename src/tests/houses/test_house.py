import pytest
from httpx import AsyncClient

from src.models import House
from src.schemas.house import HouseCreate


@pytest.mark.asyncio
async def test_read_houses(house: House, client: AsyncClient):
    response = await client.get("/houses/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
async def test_read_house_by_id(house: House, client: AsyncClient):
    response = await client.get(f"/houses/{house.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
async def test_create_house(delete_house, client: AsyncClient):
    house = {
        "cadastral_number": "11:11:1111111:11",
        "longitude": 10.00,
        "latitude": 10.00,
    }
    response = await client.post("/houses/", json=house)
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house["cadastral_number"]
    assert data["longitude"] == house["longitude"]
    assert data["latitude"] == house["latitude"]
    await delete_house(house_id=data["id"])


@pytest.mark.asyncio
async def test_delete_house(create_house: House, client: AsyncClient):
    house = HouseCreate(
        cadastral_number="11:11:1111111:11",
        longitude=10.00,
        latitude=10.00,
    )
    created_house = await create_house(house=house)
    response = await client.delete(f"/houses/{created_house.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_order_house(house: House, client: AsyncClient):
    response = await client.patch(f"/houses/{house.id}", json={"order": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
async def test_calculate_house(house: House, client: AsyncClient):
    response = await client.patch(f"/houses/calculate/{house.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number
    assert data["calculated"] is True


@pytest.mark.asyncio
async def test_validate_cadastral_number(delete_house, client: AsyncClient):
    mock_data = {
        "12:12:1234567:12": True,
        "12:1:123456:12": False,
        "12:12:sa:12": False,
        "1234:12345:1234567:12": False,
    }
    houses = [
        {
            "cadastral_number": item,
            "longitude": 10.00,
            "latitude": 10.00,
        }
        for item in mock_data.keys()
    ]
    for house in houses:
        response = await client.post("/houses/", json=house)
        if mock_data[house["cadastral_number"]]:
            assert response.status_code == 200
            data = response.json()
            assert data["cadastral_number"] == house["cadastral_number"]
            await delete_house(house_id=data["id"])
        else:
            assert response.status_code == 400
