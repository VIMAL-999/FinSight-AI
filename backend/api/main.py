from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from backend.api.users import router as users_router
from backend.api.portfolio import router as portfolio_router
from backend.api.holding import router as holding_router
from backend.api.market import router as market_router
from backend.api.advisor import router as advisor_router
from backend.api.dashboard import router as dashboard_router
from backend.api.recommendation import router as recommendation_router

# Global Exception Handler
from backend.api.exceptions import global_exception_handler

app = FastAPI(
    title="FinSight AI API",
    description="AI Financial Intelligence Platform",
    version="1.0.0"
)

# ----------------------------
# CORS Middleware
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Global Exception Handler
# ----------------------------
app.add_exception_handler(
    Exception,
    global_exception_handler
)

# ----------------------------
# Register Routers
# ----------------------------
app.include_router(users_router)
app.include_router(portfolio_router)
app.include_router(holding_router)
app.include_router(market_router)
app.include_router(advisor_router)
app.include_router(dashboard_router)
app.include_router(recommendation_router)

# ----------------------------
# Home
# ----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to FinSight AI 🚀"
    }


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
def health():
    return {
        "status": "Running"
    }