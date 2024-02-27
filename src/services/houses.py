import random
from asyncio import sleep
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.models import House
from src.schemas.house import HouseCreate
from src.services.tools import validate_cadastral_number
from src.utils.unitofwork import UnitOfWork


class HouseService:
    async def get_all_houses(self, uow: UnitOfWork) -> List[House]:
        async with uow:
            houses = await uow.houses.find_all()
            await uow.commit()
            return houses

    async def get_houses_by_id(self, house_id: int, uow: UnitOfWork) -> House:
        async with uow:
            house = await uow.houses.find_one(id=house_id)
            await uow.commit()
            return house

    async def create_house(self, house: HouseCreate, uow: UnitOfWork) -> House:
        if await validate_cadastral_number(house.cadastral_number) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cadastral number={house.cadastral_number} is not correct",
            )
        async with uow:
            try:
                house_db = await uow.houses.find_one(
                    cadastral_number=house.cadastral_number
                )
                if house_db:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"House with cadastral number={house.cadastral_number} already created",
                    )
            except NoResultFound:
                house = await uow.houses.add_one(
                    {
                        "order": random.randint(1, 10),
                        "cadastral_number": house.cadastral_number,
                        "longitude": house.longitude,
                        "latitude": house.latitude,
                    }
                )
                await uow.commit()
                return house

    async def update_order_house(
        self, order: int, house_id: int, uow: UnitOfWork
    ) -> House:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"House not found",
                )
            house_updated = await uow.houses.edit_one(
                id=house_id, data={"order": order}
            )
            await uow.commit()
            return house_updated

    async def calculate_house(self, house_id: int, uow: UnitOfWork) -> House:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"House not found",
                )
            await sleep(2)
            house_calculated = await uow.houses.edit_one(
                id=house_id, data={"calculated": True}
            )
            await uow.commit()
            return house_calculated

    async def delete_house(self, house_id: int, uow: UnitOfWork) -> str:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"House not found",
                )
            await uow.houses.delete(id=house_id)
            await uow.commit()
            return f"House was deleted"
