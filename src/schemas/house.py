from pydantic import BaseModel

from src.schemas.base import Base


class HouseBase(BaseModel):
    cadastral_number: str
    longitude: float
    latitude: float


class House(Base, HouseBase):
    order: int
    calculated: bool

    class Config:
        orm_mode = True


class HouseCreate(HouseBase):
    pass


class HouseUpdate(BaseModel):
    order: int

    class Config:
        orm_mode = True
