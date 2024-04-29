from src.models import House, User
from src.repositories.base import SQLAlchemyModelRepository


class UserModelRepository(SQLAlchemyModelRepository):
    model = User


class HouseModelRepository(SQLAlchemyModelRepository):
    model = House
