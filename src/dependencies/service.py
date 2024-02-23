from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.repositories.users import UserRepository
from src.services.users import UserService


async def create_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    user_repository: UserRepository = UserRepository(session=session)
    user_service: UserService = UserService(user_repository=user_repository)
    return user_service
