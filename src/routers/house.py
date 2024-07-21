from fastapi import APIRouter, Depends

from src.dependencies.auth import get_current_user
from src.dependencies.services.house_service_factory import HouseServiceDep
from src.models import User
from src.schemas.house import House, HouseCreate, HouseUpdate

router = APIRouter(tags=["houses"])


@router.get("/houses/", response_model=list[House])
async def read_houses(
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await house_service.get_all_houses()


@router.get("/houses/{house_id}", response_model=House)
async def read_house_by_id(
    house_id: int,
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await house_service.get_houses_by_id(house_id=house_id)


@router.post("/houses/", response_model=House, tags=["house"])
async def create_house(
    house: HouseCreate,
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await house_service.create_house(house=house)


@router.patch("/houses/{house_id}", response_model=House)
async def update_order_house(
    house_id: int,
    house: HouseUpdate,
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await house_service.update_order_house(
        order=house.order, house_id=house_id
    )


@router.patch("/houses/calculate/{house_id}", response_model=House)
async def calculate_house(
    house_id: int,
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await house_service.calculate_house(house_id=house_id)


@router.delete("/houses/{house_id}")
async def delete_house(
    house_id: int,
    house_service: HouseServiceDep,
    current_user: User = Depends(get_current_user),
) -> str:
    return await house_service.delete_house(house_id=house_id)
