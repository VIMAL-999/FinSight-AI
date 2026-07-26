from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Portfolio
from backend.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse
)

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)


# -------------------------
# Create Portfolio
# -------------------------
@router.post("/", response_model=PortfolioResponse)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db)
):

    new_portfolio = Portfolio(
        name=portfolio.name,
        balance=0
    )

    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    return new_portfolio


# -------------------------
# Get All Portfolios
# -------------------------
@router.get("/", response_model=list[PortfolioResponse])
def get_portfolios(
    db: Session = Depends(get_db)
):

    return db.query(Portfolio).all()


# -------------------------
# Get Portfolio by ID
# -------------------------
@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    return portfolio


# -------------------------
# Delete Portfolio
# -------------------------
@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    db.delete(portfolio)
    db.commit()

    return {
        "message": "Portfolio deleted successfully"
    }