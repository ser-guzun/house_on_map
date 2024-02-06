from datetime import datetime, timedelta
from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models import Token
from src.models.users import User
from src.schemas.users import UserCreate
from src.services.tools import hash_password, validate_password


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


async def authentificate_user(
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
