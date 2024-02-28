import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import create_app
from src.models import User
from src.schemas.tokens import Token
from src.schemas.users import UserCreate
from src.services.users import UserService
from src.utils.unitofwork import UnitOfWork


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture
async def unit_of_work() -> UnitOfWork:
    return UnitOfWork()


@pytest_asyncio.fixture
async def create_user(unit_of_work: UnitOfWork):
    async def wrapper(email: str, name: str, password: str) -> User:
        user = UserCreate(email=email, name=name, password=password)
        user_db = await UserService().create_user(user=user, uow=unit_of_work)
        assert user_db.email == email
        return user_db

    return wrapper


@pytest_asyncio.fixture
async def delete_user(unit_of_work: UnitOfWork):
    async def wrapper(email: str):
        return await UserService().delete_user(email=email, uow=unit_of_work)

    return wrapper


@pytest_asyncio.fixture
async def user(create_user, delete_user):
    email = "test@test.com"
    name = "test_name"
    password = "test_pass"
    user_created = await create_user(email=email, name=name, password=password)
    assert user_created.email == email
    yield user_created
    await delete_user(email=email)


@pytest_asyncio.fixture
async def auth_client(app: FastAPI, user: User, unit_of_work: UnitOfWork):
    password = "test_pass"
    token: Token = await UserService().authenticate_user_by_jwt(
        email=user.email, password=password, uow=unit_of_work
    )
    headers = {"Authorization": f"Bearer {token.access_token}"}

    async with AsyncClient(
        app=app, base_url="http://localhost:8000", headers=headers
    ) as client:
        yield client
