from sqlalchemy import select

from src.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def add(self, email, name, hash_pass):
        user = User(email=email, name=name, hashed_password=hash_pass)
        self.session.add(user)
        return user

    async def get_by_email(self, email) -> User:
        user = await self.session.execute(
            select(User).where(User.email == email)
        )
        return user.scalar()

    async def list(self):
        users = await self.session.execute(select(User))
        return users.scalars().all()
