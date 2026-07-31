from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Portfolio, Holding

from backend.schemas.dashboard import DashboardResponse

from backend.services.dashboard_service import (
    investment_score,
    diversification_warning
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/{portfolio_id}", response_model=DashboardResponse)
def dashboard(
    portfolio_id: int,
    db: Session = Depends(get_db)
):

    portfolio = db.query(
        Portfolio
    ).filter(
        Portfolio.id == portfolio_id
    ).first()

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    holdings = db.query(
        Holding
    ).filter(
        Holding.portfolio_id == portfolio_id
    ).all()

    if len(holdings) == 0:
        raise HTTPException(
            status_code=404,
            detail="No holdings found"
        )

    allocation = {}

    total_value = 0

    for h in holdings:

        value = h.current_price * h.quantity

        total_value += value

    best_stock = ""
    worst_stock = ""

    best_gain = -999999999
    worst_gain = 999999999

    total_buy = 0

    for h in holdings:

        value = h.current_price * h.quantity

        allocation[h.symbol] = value

        gain = value - (h.buy_price * h.quantity)

        if gain > best_gain:
            best_gain = gain
            best_stock = h.symbol

        if gain < worst_gain:
            worst_gain = gain
            worst_stock = h.symbol

        total_buy += (
            h.buy_price *
            h.quantity
        )

    for symbol in allocation:

        allocation[symbol] = round(
            allocation[symbol] /
            total_value *
            100,
            2
        )

    return_percentage = (
        (
            total_value -
            total_buy
        )
        /
        total_buy
    ) * 100

    return {

        "investment_score":
        investment_score(
            return_percentage,
            len(holdings)
        ),

        "total_holdings":
        len(holdings),

        "top_gainer":
        best_stock,

        "top_loser":
        worst_stock,

        "allocation":
        allocation,

        "warning":
        diversification_warning(
            allocation
        )
    }