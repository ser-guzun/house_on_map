from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.dependencies.database import get_session
from src.models import User
from src.services.user_service import get_user_by_email, get_user_by_token
from src.settings import settings

# oauth2_scheme_by_token_auth = OAuth2PasswordBearer(tokenUrl="login_by_token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_by_jwt")


# async def get_current_user_for_token_auth(
#     token: UUID = Depends(oauth2_scheme_by_token_auth),
#     session: AsyncSession = Depends(get_session),
# ) -> User:
#     user = await get_user_by_token(token=token, session=session)
#     return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(email=username, session=session)
    if user is None:
        raise credentials_exception
    return user
