from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config.settings import DATABASE_URL

# PostgreSQL Engine
engine = create_engine(
    DATABASE_URL
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Import models AFTER Base is created
from backend.database.models import User, Portfolio, Holding

# Create all tables
Base.metadata.create_all(bind=engine)