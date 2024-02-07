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


# Роут с простой парольной аутентификацией
@router.get(
    "/users_by_pass/", response_model=list[User], tags=["simple pass auth"]
)
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


# Роут с аутентификцией через обычный UUID-токен
# @router.get(
#     "/users_by_token/", response_model=list[User], tags=["simple token auth"]
# )
# async def read_token_users(
#     current_user: User = Depends(get_current_user_for_token_auth),
#     session: AsyncSession = Depends(get_session),
# ) -> list[User]:
#     if current_user.is_active is False:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )
#     users = await user_service.get_users(session=session)
#     result = [user for user in users]
#     return result


@router.post("/create_user/", response_model=User, tags=["user"])
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> User:
    return await user_service.create_user(user=user, session=session)


@router.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    return current_user


# Роут для аутентификции через обычный UUID-токен
# @router.post("/login_by_token", tags=["simple token auth"])
# async def login_by_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     session: AsyncSession = Depends(get_session),
# ) -> dict:
#     token = await user_service.authenticate_user_by_token(
#         email=form_data.username,
#         password=form_data.password,
#         session=session,
#     )
#     return {"access_token": token.token, "token_type": "bearer"}


@router.post("/login_by_jwt")
async def login_by_jwt(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> dict:
    token = await user_service.authenticate_user_by_jwt(
        email=form_data.username,
        password=form_data.password,
        session=session,
    )
    print(token)
    return {"access_token": token.access_token, "token_type": "bearer"}
