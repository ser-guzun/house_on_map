import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.dependencies.database import get_session
from src.main import app

# Для запуска тестов без развертывания приложения в докер-контейнере
DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
test_async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


async def override_get_session():
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.mark.asyncio
async def test_read_houses(house, client: AsyncClient):
    response = await client.get("/houses/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["cadastral_number"] == house["cadastral_number"]


@pytest.mark.asyncio
async def test_read_house_by_id(house, client: AsyncClient):
    response = await client.get(f"/houses/{house['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house["cadastral_number"]


@pytest.mark.asyncio
async def test_create_house(delete_house, client: AsyncClient):
    house = {
        "cadastral_number": "10000",
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
async def test_delete_house(create_house, client: AsyncClient):
    house = {
        "cadastral_number": "10000",
        "longitude": 10.00,
        "latitude": 10.00,
    }
    created_house = await create_house(house=house)
    response = await client.delete(f"/houses/{created_house['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_order_house(house, client: AsyncClient):
    response = await client.put(f"/houses/{house['id']}", json={"order": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house["cadastral_number"]


@pytest.mark.asyncio
async def test_calculate_house(house, client: AsyncClient):
    response = await client.put(f"/houses/calculate/{house['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["cadastral_number"] == house["cadastral_number"]
