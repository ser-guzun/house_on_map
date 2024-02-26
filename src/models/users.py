from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from src.dependencies.database import Base
from src.models.base import BaseModel


class User(Base, BaseModel):
    """Пользователь"""

    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Пользователь {self.__dict__}>"
