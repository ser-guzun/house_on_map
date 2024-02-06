import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.dependencies.database import Base
from src.models.base import BaseModel


class Token(Base, BaseModel):
    """Токен доступа"""

    __tablename__ = "tokens"

    token = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    expires = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="tokens")

    def __repr__(self):
        return f"<Токен {self.__dict__}>"
