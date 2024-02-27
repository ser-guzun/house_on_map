from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from src.dependencies.service import UOWDep
from src.models import User
from src.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_by_jwt")


async def get_current_user(
    uow: UOWDep,
    token: str = Depends(oauth2_scheme),
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
    async with uow:
        user = await uow.users.find_one(email=username)
    if user is None:
        raise credentials_exception
    return user
