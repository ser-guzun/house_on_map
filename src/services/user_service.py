from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models.users import User
from src.repositories.users import UserRepository
from src.schemas.tokens import Token
from src.schemas.users import UserCreate
from src.services.tools import hash_password, validate_password
from src.settings import settings


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    repo = UserRepository(session)
    db_user = await repo.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already created",
        )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = await hash_password(
        context=pwd_context, password=user.password
    )
    user = await repo.create_user(
        email=user.email, name=user.name, hash_pass=hashed_password
    )
    await session.commit()
    return user


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
    repo = UserRepository(session)
    user = await repo.get_user_by_email(email=email)
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
    return Token(access_token=access_token, token_type="bearer")
