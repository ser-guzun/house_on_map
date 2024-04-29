import pytest
from httpx import AsyncClient

from src.models import House
from src.schemas.house import HouseCreate


@pytest.mark.asyncio
async def test_read_houses(house: House, auth_client: AsyncClient):
    response = await auth_client.get("/houses/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
async def test_read_house_by_id(house: House, auth_client: AsyncClient):
    response = await auth_client.get(f"/houses/{house.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
@pytest.mark.parametrize("cad_number", ["12:12:1234567:12"])
async def test_create_house(
    delete_house, auth_client: AsyncClient, cad_number: str
):
    house = {
        "cadastral_number": cad_number,
        "longitude": 10.00,
        "latitude": 10.00,
    }
    response = await auth_client.post("/houses/", json=house)
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house["cadastral_number"]
    assert data["longitude"] == house["longitude"]
    assert data["latitude"] == house["latitude"]
    await delete_house(house_id=data["id"])


@pytest.mark.asyncio
@pytest.mark.parametrize("cad_number", ["12:12:1234567:12"])
async def test_delete_house(
    create_house: House, auth_client: AsyncClient, cad_number: str
):
    house = HouseCreate(
        cadastral_number=cad_number,
        longitude=10.00,
        latitude=10.00,
    )
    created_house = await create_house(house=house)
    response = await auth_client.delete(f"/houses/{created_house.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_order_house(house: House, auth_client: AsyncClient):
    response = await auth_client.patch(f"/houses/{house.id}", json={"order": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number


@pytest.mark.asyncio
async def test_calculate_house(house: House, auth_client: AsyncClient):
    response = await auth_client.patch(f"/houses/calculate/{house.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house.cadastral_number
    assert data["calculated"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cad_number",
    [
        ("12:12:1234567:12",),
        ("12:1:123456:12",),
        ("12:12:sa:12",),
        ("1234:12345:1234567:12",),
    ],
)
async def test_validate_cadastral_number(
    delete_house, auth_client: AsyncClient, cad_number: str
):
    house = {
        "cadastral_number": cad_number,
        "longitude": 10.00,
        "latitude": 10.00,
    }
    response = await auth_client.post("/houses/", json=house)
    if response.status_code == 200:
        assert response.status_code == 200
        data = response.json()
        assert data["cadastral_number"] == house["cadastral_number"]
        await delete_house(house_id=data["id"])
    elif response.status_code == 422:
        assert response.status_code == 422
