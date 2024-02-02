from sqlalchemy import Boolean, Column, Float, Integer, String

from src.dependencies.database import Base
from src.models.base import MyBaseModel


class House(Base, MyBaseModel):
    """Дом, объект недвижимости"""

    __tablename__ = "house"

    # Подрядок запроса на вычисление
    order = Column(Integer, autoincrement=True, nullable=False)

    cadastral_number = Column(String, nullable=False, unique=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    calculated = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Дом {self.__dict__}>"
