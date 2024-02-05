from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.models import User
from src.services.user_service import get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: UUID = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await get_user_by_token(token=token, session=session)
    return user
