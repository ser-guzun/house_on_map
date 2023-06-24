import random

from anyio import sleep
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models.house import House
from src.schemas.house import HouseCreate


async def get_houses(session: AsyncSession) -> list[House]:
    houses = await session.execute(select(House))
    return houses.scalars().all()


async def get_house_by_id(house_id: int, session: AsyncSession) -> House:
    house = await session.execute(select(House).where(House.id == house_id))
    return house.scalar()


async def get_house_by_cad_number(
    cadastral_number: str, session: AsyncSession
) -> House:
    house = await session.execute(
        select(House).where(House.cadastral_number == cadastral_number)
    )
    return house.scalar()


async def create_house(house: HouseCreate, session: AsyncSession) -> House:
    house = House(
        order=random.randint(1, 10),
        cadastral_number=house.cadastral_number,
        longitude=house.longitude,
        latitude=house.latitude,
    )
    session.add(house)
    await session.commit()
    return house


async def update_order_house(
    order: int, house: House, session: AsyncSession
) -> House:
    house.order = order
    session.add(house)
    await session.commit()
    return house


async def calculate_house(house: House, session: AsyncSession) -> House:
    await sleep(random.randint(10, 60))
    house.calculated = True
    session.add(house)
    await session.commit()
    return house


async def delete_house(house_id: int, session: AsyncSession) -> House:
    house = await session.execute(select(House).where(House.id == house_id))
    house = house.scalar()
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with this id: {id} not found",
        )
    await session.delete(house)
    await session.commit()
    return house
