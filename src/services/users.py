from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.models import User
from src.schemas.tokens import Token
from src.schemas.users import UserCreate
from src.settings import settings
from src.utils.unitofwork import UnitOfWork


class UserService:
    async def get_all_users(self, uow: UnitOfWork) -> List[User]:
        async with uow:
            users = await uow.users.find_all()
            await uow.commit()
            return users

    async def create_user(self, user: UserCreate, uow: UnitOfWork) -> User:
        async with uow:
            try:
                user_db = await uow.users.find_one(email=user.email)
                if user_db:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User already created",
                    )
            except NoResultFound:
                pwd_context = CryptContext(
                    schemes=["bcrypt"], deprecated="auto"
                )
                hashed_password = await self._hash_password(
                    context=pwd_context, password=user.password
                )

                user = await uow.users.add_one(
                    {
                        "email": user.email,
                        "name": user.name,
                        "hashed_password": hashed_password,
                    }
                )
                await uow.commit()
                return user

    @staticmethod
    async def delete_user(email: str, uow: UnitOfWork):
        async with uow:
            try:
                await uow.users.find_one(email=email)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found",
                )
            await uow.users.delete(email=email)
            await uow.commit()
            return f"User was deleted"

    @staticmethod
    async def _create_jwt_token(
        data: dict, expires_delta: timedelta | None = None
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
        self, email: str, password: str, uow: UnitOfWork
    ) -> Token:
        async with uow:
            credentials_exception = HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Incorrect email or password",
            )
            user_db = await uow.users.find_one(email=email)
            if not user_db:
                raise credentials_exception

            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if not await self._validate_password(
                pwd_context, password, user_db.hashed_password
            ):
                raise credentials_exception
            access_token = await self._create_jwt_token(
                data={"sub": user_db.email},
                expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def _validate_password(
        context: CryptContext, password: str, hashed_password: str
    ) -> bool:
        return context.verify(password, hashed_password)

    @staticmethod
    async def _hash_password(context: CryptContext, password: str) -> str:
        return context.hash(password)
