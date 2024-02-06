from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.database import get_session
from src.models.user import Token, User
from src.services.user import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from src.settings import settings

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/items/me", response_model=User, tags=["oauth"])
async def read_users_me(
    current_user: Annotated[str, Depends(get_current_active_user)]
):
    return current_user


@router.post("/token", response_model=Token, tags=["oauth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(
        settings.USERS_DB, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
