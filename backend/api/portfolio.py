from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Portfolio, Holding

from backend.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse
)

from backend.schemas.summary import PortfolioSummary

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


# -------------------------
# Portfolio Summary
# -------------------------
@router.get(
    "/{portfolio_id}/summary",
    response_model=PortfolioSummary
)
def portfolio_summary(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id
    ).first()

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    holdings = db.query(Holding).filter(
        Holding.portfolio_id == portfolio_id
    ).all()

    total_investment = 0
    current_value = 0

    for holding in holdings:

        investment = (
            holding.buy_price *
            holding.quantity
        )

        value = (
            holding.current_price *
            holding.quantity
        )

        total_investment += investment
        current_value += value

    profit_loss = current_value - total_investment

    if total_investment == 0:
        return_percentage = 0
    else:
        return_percentage = (
            profit_loss /
            total_investment
        ) * 100

    return {
        "portfolio_name": portfolio.name,
        "total_investment": round(total_investment, 2),
        "current_value": round(current_value, 2),
        "profit_loss": round(profit_loss, 2),
        "return_percentage": round(return_percentage, 2)
    }