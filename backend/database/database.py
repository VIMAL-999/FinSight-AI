from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------
# PostgreSQL Connection
# -----------------------------------
DATABASE_URL = "postgresql://postgres:FinSight%40123@localhost:5432/finsight_db"

# -----------------------------------
# SQLAlchemy Engine
# -----------------------------------
engine = create_engine(DATABASE_URL)

# -----------------------------------
# Session Factory
# -----------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------
# Base Class
# -----------------------------------
Base = declarative_base()

# -----------------------------------
# Import Models
# -----------------------------------
from backend.database.models import (
    User,
    Portfolio,
    Holding
)

# -----------------------------------
# Create Tables
# -----------------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------------
# Database Dependency
# -----------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()