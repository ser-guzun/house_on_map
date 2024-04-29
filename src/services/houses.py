import random
from asyncio import sleep
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.models import House
from src.schemas.house import HouseCreate
from src.utils.exceptions import HouseNotFoundException
from src.utils.unitofwork import PgUnitOfWork


class HouseService:
    async def get_all_houses(self, uow: PgUnitOfWork) -> List[House]:
        async with uow:
            houses = await uow.houses.find_all()
            await uow.commit()
            return houses

    async def get_houses_by_id(self, house_id: int, uow: PgUnitOfWork) -> House:
        async with uow:
            house = await uow.houses.find_one(id=house_id)
            await uow.commit()
            return house

    async def create_house(
        self, house: HouseCreate, uow: PgUnitOfWork
    ) -> House:
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
        self, order: int, house_id: int, uow: PgUnitOfWork
    ) -> House:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HouseNotFoundException()
            house_updated = await uow.houses.edit_one(
                id=house_id, data={"order": order}
            )
            await uow.commit()
            return house_updated

    async def calculate_house(self, house_id: int, uow: PgUnitOfWork) -> House:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HouseNotFoundException()
            await sleep(2)
            house_calculated = await uow.houses.edit_one(
                id=house_id, data={"calculated": True}
            )
            await uow.commit()
            return house_calculated

    async def delete_house(self, house_id: int, uow: PgUnitOfWork) -> str:
        async with uow:
            try:
                await uow.houses.find_one(id=house_id)
            except NoResultFound:
                raise HouseNotFoundException()
            await uow.houses.delete(id=house_id)
            await uow.commit()
            return "House was deleted"
