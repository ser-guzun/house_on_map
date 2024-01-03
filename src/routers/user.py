from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.database import get_session
from src.models.user import UserInDB
from src.services.user import fake_hash_password, get_current_active_user
from src.settings import settings

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/items/me", tags=["oauth"])
async def read_users_me(
    current_user: Annotated[str, Depends(get_current_active_user)]
):
    return current_user


@router.post("/token", tags=["oauth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = settings.USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    return {"access_token": user.username, "token_type": "bearer"}
