from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create_user(self, email, name, hash_pass):
        user = User(email=email, name=name, hashed_password=hash_pass)
        self.session.add(user)
        return user

    async def get_user_by_email(self, email) -> User:
        user = await self.session.execute(
            select(User).where(User.email == email)
        )
        return user.scalar()

    async def list_users(self):
        users = await self.session.execute(select(User))
        return users.scalars().all()

    async def delete_user(self, email):
        user = await self.get_user_by_email(email=email)
        if user:
            await self.session.delete(user)
