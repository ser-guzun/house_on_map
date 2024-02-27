import random

from anyio import sleep
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models.house import House


async def _get_house_by_cad_number(
    cadastral_number: str, session: AsyncSession
) -> House:
    house = await session.execute(
        select(House).where(House.cadastral_number == cadastral_number)
    )
    return house.scalar()


async def calculate_house(house_id: int, session: AsyncSession) -> House:
    house = await session.execute(select(House).where(House.id == house_id))
    house = house.scalar()
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"House with id={house_id} not found",
        )
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
            detail=f"House with id={house_id} not found",
        )
    await session.delete(house)
    await session.commit()
    return house
