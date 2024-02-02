from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.schemas.users import User, UserCreate
from src.services import user_service

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/users/", response_model=list[User], tags=["user"])
async def read_users(
    email: EmailStr,
    password: str,
    session: AsyncSession = Depends(get_session),
) -> list[User]:
    result = []
    if await user_service.validate_user(email, password, session):
        users = await user_service.get_users(session=session)
        result = [user for user in users]
    return result


@router.post("/sign-up/", response_model=User, tags=["user"])
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> User:
    return await user_service.create_user(user=user, session=session)
