from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    balance = Column(Float, default=0)

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship("User")