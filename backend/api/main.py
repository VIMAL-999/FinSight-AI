from fastapi import FastAPI

from backend.api.users import router as users_router
from backend.api.portfolio import router as portfolio_router

app = FastAPI(
    title="FinSight AI API",
    description="AI Financial Intelligence Platform",
    version="1.0.0"
)

# Register Routers
app.include_router(users_router)
app.include_router(portfolio_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to FinSight AI 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "Running"
    }