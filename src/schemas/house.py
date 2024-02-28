from pydantic import BaseModel, validator

from src.schemas.base import SchemaBase
from src.services.tools import validate_cadastral_number


class HouseBase(BaseModel):
    cadastral_number: str
    longitude: float
    latitude: float

    @validator("cadastral_number")
    def check_cadastral_number(cls, number: str):
        if validate_cadastral_number(number) is False:
            raise ValueError("Cadastral number is not correct")
        return number


class House(SchemaBase, HouseBase):
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
