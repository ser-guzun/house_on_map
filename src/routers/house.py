from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_session
from src.schemas.house import House, HouseCreate
from src.services import house_service

router = APIRouter(dependencies=[Depends(get_session)])


# @router.get("/cities/", response_model=list[City], tags=["city"])
# async def read_cities(
#     session: AsyncSession = Depends(get_session),
# ) -> list[City]:
#     cities = await city_service.get_cities(session=session)
#     return [city for city in cities]


# @router.get("/cities/{city_id}", response_model=City, tags=["city"])
# async def read_city_by_id(
#     city_id: int, session: AsyncSession = Depends(get_session)
# ) -> City:
#     city = await city_service.get_city_by_id(city_id=city_id, session=session)
#     return city


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
