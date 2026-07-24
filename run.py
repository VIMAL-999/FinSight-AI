import uvicorn

from backend.api.main import app
from backend.database.database import engine
from backend.database.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )