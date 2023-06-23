from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, func

from src.dependencies.database import Base


class House(Base):
    """Дом, объект недвижимости"""

    __tablename__ = "house"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Подрядок запроса на вычисление
    order = Column(Integer, autoincrement=True, nullable=False)

    cadastral_number = Column(String, nullable=False, unique=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    calculated = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        DateTime(timezone=False), nullable=False, default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=False), nullable=False, default=func.now()
    )

    def __repr__(self):
        return f"<Дом {self.id}>"
