import pytest
from httpx import AsyncClient

from src.models import User
from src.schemas.users import UserCreate


@pytest.mark.asyncio
async def test_get_all_users(auth_client: AsyncClient, user: User):
    response = await auth_client.get(url="/users/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["email"] == user.email
    assert data[0]["name"] == user.name


@pytest.mark.asyncio
async def test_create_user(auth_client, delete_user):
    email = "test_create_user@test.com"
    name = "test_name"
    password = "test_pass"
    user: UserCreate = UserCreate(email=email, name=name, password=password)
    response = await auth_client.post(url="/create_user/", json=user.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["name"] == name
    await delete_user(email=email)


@pytest.mark.asyncio
async def test_delete_user(auth_client, create_user):
    email = "test_delete_user@test.com"
    await create_user(email=email, name="test", password="pass")
    response = await auth_client.delete(url=f"/users/{email}")
    assert response.status_code == 200
