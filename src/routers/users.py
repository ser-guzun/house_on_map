import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.schemas.users import User, UserCreate
from src.services import user_service

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/users/", response_model=list[User], tags=["simple pass auth"])
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
) -> dict:
    token = await user_service.authentificate_user(
        email=form_data.username,
        password=form_data.password,
        session=session,
    )
    return {"access_token": token.token, "token_type": "bearer"}


@router.get(
    "/token_users/", response_model=list[User], tags=["simple token auth"]
)
async def read_token_users(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[User]:
    if current_user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    users = await user_service.get_users(session=session)
    result = [user for user in users]
    return result
