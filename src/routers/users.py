from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.dependencies.service import create_user_service
from src.schemas.users import User, UserCreate
from src.services.users import UserService

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/users/", response_model=List[User], tags=["simple pass auth"])
async def read_users(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(create_user_service),
) -> List[User]:
    return await user_service.get_all_users()


@router.post("/create_user/", response_model=User, tags=["user"])
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(create_user_service),
    current_user: User = Depends(get_current_user),
) -> User:
    return await user_service.create_user(user=user)


@router.delete("/users/{email}", tags=["user"])
async def delete_user(
    email: str, user_service: UserService = Depends(create_user_service)
):
    return await user_service.delete_user(email=email)


@router.get("/current_user/")
async def read_items(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login_by_jwt")
async def login_by_jwt(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(create_user_service),
) -> dict:
    token = await user_service.authenticate_user_by_jwt(
        email=form_data.username, password=form_data.password
    )
    return {"access_token": token.access_token, "token_type": "bearer"}
