from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from src.models import User
from src.repositories.users import UserRepository
from src.schemas.users import UserCreate
from src.services.tools import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository: UserRepository = user_repository

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.list_users()

    async def create_user(self, user: UserCreate) -> User:
        db_user = await self.user_repository.get_user_by_email(email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already created",
            )
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = await hash_password(
            context=pwd_context, password=user.password
        )
        user = await self.user_repository.create_user(
            email=user.email, name=user.name, hash_pass=hashed_password
        )
        await self.user_repository.session.commit()
        return user

    async def delete_user(self, email: str):
        await self.user_repository.delete_user(email=email)
        return await self.user_repository.session.commit()
