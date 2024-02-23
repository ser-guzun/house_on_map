import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import create_app
from src.schemas.users import UserCreate


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app) as client:
        yield client


@pytest_asyncio.fixture
async def create_user(client: AsyncClient):
    async def wrapper(email: str, name: str, password: str):
        base_url = "http://localhost:8000"
        user: UserCreate = UserCreate(email=email, name=name, password=password)
        response = await client.post(
            url=base_url + "/create_user/", json=user.dict()
        )
        assert response.status_code == 200
        return response.json()

    return wrapper


@pytest_asyncio.fixture
async def delete_user(client):
    async def wrapper(email: str):
        base_url = "http://localhost:8000"
        response = await client.delete(url=f"{base_url}/users/{email}")
        assert response.status_code == 200

    return wrapper


@pytest_asyncio.fixture
async def user(create_user, delete_user):
    email = "test@test.com"
    name = "test_name"
    password = "test_pass"
    user_created = await create_user(email=email, name=name, password=password)
    yield user_created
    await delete_user(email=email)
