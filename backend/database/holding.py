from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)

    portfolio_id = Column(
        Integer,
        ForeignKey("portfolios.id"),
        nullable=False
    )

    symbol = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

    quantity = Column(Float, nullable=False)

    buy_price = Column(Float, nullable=False)

    current_price = Column(Float, nullable=False)