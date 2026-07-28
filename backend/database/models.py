from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database.database import Base


# -------------------------
# User Model
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


# -------------------------
# Portfolio Model
# -------------------------
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)


# -------------------------
# Holding Model
# -------------------------
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