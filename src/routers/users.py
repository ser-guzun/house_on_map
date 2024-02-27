from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.dependencies.service import UOWDep
from src.schemas.users import User, UserCreate
from src.services.users import UserService

router = APIRouter(
    dependencies=[Depends(get_session)],
    # prefix="/users",
    tags=["Users"],
)


@router.get("/users/", response_model=List[User])
async def read_users(
    uow: UOWDep,
    # current_user: User = Depends(get_current_user),
) -> List[User]:
    return await UserService().get_all_users(uow=uow)


@router.post("/create_user/", response_model=User)
async def create_user(
    user: UserCreate,
    uow: UOWDep,
    # current_user: User = Depends(get_current_user),
) -> User:
    return await UserService().create_user(user=user, uow=uow)


@router.delete("/users/{email}")
async def delete_user(email: str, uow: UOWDep) -> str:
    return await UserService().delete_user(email=email, uow=uow)


@router.post("/login_by_jwt")
async def login_by_jwt(
    uow: UOWDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    token = await UserService().authenticate_user_by_jwt(
        email=form_data.username, password=form_data.password, uow=uow
    )
    return {"access_token": token.access_token, "token_type": "bearer"}
