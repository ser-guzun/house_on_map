import pytest

from src.schemas.users import UserCreate


@pytest.mark.asyncio
async def test_get_all_users(client, user):
    response = await client.get(url="http://localhost:8000/users/")
    assert response.status_code == 200
    data = response.json()
    assert data[-1]["email"] == "test@test.com"
    assert data[-1]["name"] == "test_name"


@pytest.mark.asyncio
async def test_create_user(client, delete_user):
    base_url = "http://localhost:8000"
    email = "test@test.com"
    name = "test_name"
    password = "test_pass"
    user: UserCreate = UserCreate(email=email, name=name, password=password)
    response = await client.post(
        url=base_url + "/create_user/", json=user.dict()
    )
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
    response = await client.delete(url=f"{base_url}/users/{email}")
    assert response.status_code == 200