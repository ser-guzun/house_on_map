from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.schemas.house import House, HouseCreate, HouseUpdate
from src.services import house_service

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/houses/", response_model=list[House], tags=["house"])
async def read_houses(
    session: AsyncSession = Depends(get_session),
) -> list[House]:
    houses = await house_service.get_houses(session=session)
    return [house for house in houses]


@router.get("/houses/{house_id}", response_model=House, tags=["house"])
async def read_house_by_id(
    house_id: int, session: AsyncSession = Depends(get_session)
) -> House:
    house = await house_service.get_house_by_id(
        house_id=house_id, session=session
    )
    return house


@router.post("/houses/", response_model=House, tags=["house"])
async def create_house(
    house: HouseCreate, session: AsyncSession = Depends(get_session)
) -> House:
    return await house_service.create_house(house=house, session=session)


@router.put("/houses/{house_id}", response_model=House, tags=["house"])
async def update_order_house(
    house_id: int,
    house: HouseUpdate,
    session: AsyncSession = Depends(get_session),
) -> House:
    return await house_service.update_order_house(
        order=house.order, house_id=house_id, session=session
    )


@router.put(
    "/houses/calculate/{house_id}", response_model=House, tags=["house"]
)
async def calculate_house(
    house_id: int, session: AsyncSession = Depends(get_session)
) -> House:
    return await house_service.calculate_house(
        house_id=house_id, session=session
    )


@router.delete("/houses/{house_id}", response_model=House, tags=["house"])
async def delete_house(
    house_id: int, session: AsyncSession = Depends(get_session)
) -> House:
    return await house_service.delete_house(house_id=house_id, session=session)
