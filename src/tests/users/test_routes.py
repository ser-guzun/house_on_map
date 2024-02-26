import pytest
from httpx import AsyncClient

from src.models import User
from src.schemas.users import UserCreate


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient, user: User):
    response = await client.get(url="/users/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["email"] == user.email
    assert data[0]["name"] == user.name


@pytest.mark.asyncio
async def test_create_user(client, delete_user):
    base_url = "http://localhost:8000"
    email = "test@test.com"
    name = "test_name"
    password = "test_pass"
    user: UserCreate = UserCreate(email=email, name=name, password=password)
    response = await client.post(url="/create_user/", json=user.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["name"] == name
    await delete_user(email=email)


@pytest.mark.asyncio
async def test_delete_user(client, create_user):
    base_url = "http://localhost:8000"
    email = "test@test.com"
    await create_user(email=email, name="test", password="pass")
    response = await client.delete(url=f"/users/{email}")
    assert response.status_code == 200
