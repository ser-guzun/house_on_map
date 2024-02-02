from sqlalchemy import Column, DateTime, Integer, func


class MyBaseModel:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=False), nullable=False, default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=False), nullable=False, default=func.now()
    )
