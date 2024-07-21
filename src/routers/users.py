from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.auth import get_current_user
from src.dependencies.services.user_service_factory import UserServiceDep
from src.schemas.users import User, UserCreate

router = APIRouter(tags=["Users"])


@router.get("/users/", response_model=List[User])
async def read_users(
    user_service: UserServiceDep,
    current_user: User = Depends(get_current_user),
) -> List[User]:
    return await user_service.get_all_users()


@router.post("/create_user/", response_model=User)
async def create_user(
    user: UserCreate,
    user_service: UserServiceDep,
    # current_user: User = Depends(get_current_user),
) -> User:
    return await user_service.create_user(user=user)


@router.delete("/users/{email}")
async def delete_user(
    email: str,
    user_service: UserServiceDep,
    current_user: User = Depends(get_current_user),
) -> str:
    return await user_service.delete_user(email=email)


@router.post("/login_by_jwt")
async def login_by_jwt(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    token = await user_service.authenticate_user_by_jwt(
        email=form_data.username,
        password=form_data.password,
    )
    return {"access_token": token.access_token, "token_type": "bearer"}
