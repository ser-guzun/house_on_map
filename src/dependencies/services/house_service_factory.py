from typing import Annotated

from fastapi import Depends

from src.dependencies.uows.pg_uow_factory import PgUnitOfWorkDep
from src.services.houses import HouseService


def create_house_service(uow: PgUnitOfWorkDep) -> HouseService:
    return HouseService(uow=uow)


HouseServiceDep = Annotated[HouseService, Depends(create_house_service)]
