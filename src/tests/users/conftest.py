import pytest_asyncio

from src.models import User
from src.schemas.users import UserCreate
from src.services.users import UserService
from src.utils.unitofwork import UnitOfWork


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
