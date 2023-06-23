from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.schemas.house import House, HouseCreate
from src.services import house_service

router = APIRouter(dependencies=[Depends(get_session)])


@router.get("/houses/", response_model=list[House], tags=["house"])
async def read_houses(
    session: AsyncSession = Depends(get_session),
) -> list[House]:
    houses = await house_service.get_houses(session=session)
    return [house for house in houses]


@router.get("/houses/{city_id}", response_model=House, tags=["house"])
async def read_city_by_id(
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
    db_house = await house_service.get_house_by_cad_number(
        cadastral_number=house.cadastral_number, session=session
    )
    if db_house:
        raise HTTPException(status_code=400, detail="house already created")
    return await house_service.create_house(house=house, session=session)
