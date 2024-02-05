from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.auth import get_current_user
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


@router.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    if user_service.validate_user(
        email=form_data.username,
        password=form_data.password,
        session=session,
    ):
        return {"access_token": form_data.username, "token_type": "bearer"}
