from datetime import datetime, timedelta, timezone
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models.users import User
from src.schemas.tokens import Token
from src.schemas.users import UserCreate
from src.services.tools import hash_password, validate_password
from src.settings import settings


async def get_users(session: AsyncSession) -> Sequence[User]:
    users = await session.execute(select(User))
    return users.scalars().all()


async def get_user_by_email(email: EmailStr, session: AsyncSession) -> User:
    user = await session.execute(select(User).where(User.email == email))
    return user.scalar()


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    db_user = await get_user_by_email(email=user.email, session=session)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already created",
        )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = await hash_password(
        context=pwd_context, password=user.password
    )
    user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
    )
    session.add(user)
    await session.commit()
    return user


# Simple pass auth
async def validate_user(
    email: EmailStr,
    password: str,
    session: AsyncSession,
) -> bool:
    user = await get_user_by_email(email=email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not await validate_password(pwd_context, password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorized",
        )
    return True


async def create_user_token(user_id: int, session: AsyncSession) -> Token:
    token = Token(
        expires=datetime.now() + timedelta(hours=2),
        user_id=user_id,
    )
    session.add(token)
    await session.commit()
    return token


async def get_user_by_token(token: UUID, session: AsyncSession) -> User:
    user = await session.execute(
        select(User, Token)
        .join(Token, User.id == Token.user_id)
        .where(and_(Token.token == token, Token.expires > datetime.now()))
    )
    return user.scalar()


async def get_token_by_user_id(user_id: int, session: AsyncSession) -> Token:
    token = await session.execute(
        select(Token).where(
            and_(Token.user_id == user_id, Token.expires > datetime.now())
        )
    )
    return token.scalar()


async def authenticate_user_by_token(
    email: str,
    password: str,
    session: AsyncSession,
) -> Token:
    user = await get_user_by_email(email=email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incorrect email or password",
        )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not await validate_password(pwd_context, password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incorrect email or password",
        )

    token = await get_token_by_user_id(user_id=user.id, session=session)
    if not token:
        token = await create_user_token(user_id=user.id, session=session)
    return token


async def create_jwt_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


async def authenticate_user_by_jwt(
    email: str,
    password: str,
    session: AsyncSession,
) -> Token:
    user = await get_user_by_email(email=email, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incorrect email or password",
        )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not await validate_password(pwd_context, password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incorrect email or password",
        )
    access_token = await create_jwt_token(
        data={"sub": user.email},
        expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    print(access_token)
    return Token(access_token=access_token, token_type="bearer")
