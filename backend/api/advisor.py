from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Portfolio, Holding

from backend.schemas.advisor import AdvisorResponse

from backend.services.advisor_service import (
    calculate_health,
    calculate_risk,
    diversification_score,
    recommendation
)

router = APIRouter(
    prefix="/advisor",
    tags=["AI Advisor"]
)


@router.get("/{portfolio_id}", response_model=AdvisorResponse)
def advisor(
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

    if len(holdings) == 0:
        raise HTTPException(
            status_code=404,
            detail="No holdings found"
        )

    total_buy = 0
    total_current = 0

    best_stock = None
    best_return = -999999

    worst_stock = None
    worst_return = 999999

    for h in holdings:

        investment = h.buy_price * h.quantity
        current = h.current_price * h.quantity

        total_buy += investment
        total_current += current

        gain = current - investment

        if gain > best_return:
            best_return = gain
            best_stock = h.symbol

        if gain < worst_return:
            worst_return = gain
            worst_stock = h.symbol

    return_percentage = (
        (total_current - total_buy)
        / total_buy
    ) * 100

    return {

        "portfolio_health":
            calculate_health(return_percentage),

        "risk_level":
            calculate_risk(len(holdings)),

        "diversification_score":
            diversification_score(len(holdings)),

        "best_performer":
            best_stock,

        "worst_performer":
            worst_stock,

        "recommendation":
            recommendation(return_percentage)
    }