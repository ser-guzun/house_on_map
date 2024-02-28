from fastapi import APIRouter, Depends

from src.dependencies.database import get_session
from src.dependencies.service import UOWDep
from src.schemas.house import House, HouseCreate, HouseUpdate
from src.services.houses import HouseService

router = APIRouter()


@router.get("/houses/", response_model=list[House], tags=["house"])
async def read_houses(uow: UOWDep) -> list[House]:
    return await HouseService().get_all_houses(uow=uow)


@router.get("/houses/{house_id}", response_model=House, tags=["house"])
async def read_house_by_id(house_id: int, uow: UOWDep) -> House:
    return await HouseService().get_houses_by_id(house_id=house_id, uow=uow)


@router.post("/houses/", response_model=House, tags=["house"])
async def create_house(house: HouseCreate, uow: UOWDep) -> House:
    return await HouseService().create_house(house=house, uow=uow)


@router.patch("/houses/{house_id}", response_model=House, tags=["house"])
async def update_order_house(
    house_id: int,
    house: HouseUpdate,
    uow: UOWDep,
) -> House:
    return await HouseService().update_order_house(
        order=house.order, house_id=house_id, uow=uow
    )


@router.patch(
    "/houses/calculate/{house_id}", response_model=House, tags=["house"]
)
async def calculate_house(house_id: int, uow: UOWDep) -> House:
    return await HouseService().calculate_house(house_id=house_id, uow=uow)


@router.delete("/houses/{house_id}", tags=["house"])
async def delete_house(house_id: int, uow: UOWDep) -> str:
    return await HouseService().delete_house(house_id=house_id, uow=uow)
