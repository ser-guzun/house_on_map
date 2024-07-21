from typing import Annotated

from fastapi import Depends

from src.dependencies.uows.pg_uow_factory import PgUnitOfWorkDep
from src.services.users import UserService


def create_user_service(uow: PgUnitOfWorkDep) -> UserService:
    return UserService(uow=uow)


UserServiceDep = Annotated[UserService, Depends(create_user_service)]
