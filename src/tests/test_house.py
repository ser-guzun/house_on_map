import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.dependencies.database import get_session
from src.main import app

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
