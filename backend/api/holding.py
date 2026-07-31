from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Holding, Portfolio
from backend.schemas.holding import HoldingCreate, HoldingResponse

from backend.services.stock_service import get_live_price

router = APIRouter(
    prefix="/holdings",
    tags=["Holdings"]
)


# -------------------------
# Create Holding
# -------------------------
@router.post("/", response_model=HoldingResponse)
def create_holding(
    holding: HoldingCreate,
    db: Session = Depends(get_db)
):

    portfolio = db.query(Portfolio).filter(
        Portfolio.id == holding.portfolio_id
    ).first()

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )

    new_holding = Holding(
        portfolio_id=holding.portfolio_id,
        symbol=holding.symbol.upper(),
        company_name=holding.company_name,
        quantity=holding.quantity,
        buy_price=holding.buy_price,
        current_price=holding.current_price
    )

    db.add(new_holding)
    db.commit()
    db.refresh(new_holding)

    return new_holding


# -------------------------
# Get All Holdings
# -------------------------
@router.get("/", response_model=list[HoldingResponse])
def get_holdings(
    db: Session = Depends(get_db)
):

    return db.query(Holding).all()


# -------------------------
# Get Holding By ID
# -------------------------
@router.get("/{holding_id}", response_model=HoldingResponse)
def get_holding(
    holding_id: int,
    db: Session = Depends(get_db)
):

    holding = db.query(Holding).filter(
        Holding.id == holding_id
    ).first()

    if holding is None:
        raise HTTPException(
            status_code=404,
            detail="Holding not found"
        )

    return holding


# -------------------------
# Delete Holding
# -------------------------
@router.delete("/{holding_id}")
def delete_holding(
    holding_id: int,
    db: Session = Depends(get_db)
):

    holding = db.query(Holding).filter(
        Holding.id == holding_id
    ).first()

    if holding is None:
        raise HTTPException(
            status_code=404,
            detail="Holding not found"
        )

    db.delete(holding)
    db.commit()

    return {
        "message": "Holding deleted successfully"
    }


# -------------------------
# Refresh Live Stock Price
# -------------------------
@router.put("/{holding_id}/refresh")
def refresh_stock_price(
    holding_id: int,
    db: Session = Depends(get_db)
):

    holding = db.query(Holding).filter(
        Holding.id == holding_id
    ).first()

    if holding is None:
        raise HTTPException(
            status_code=404,
            detail="Holding not found"
        )

    live_price = get_live_price(holding.symbol)

    if live_price is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to fetch live market price"
        )

    holding.current_price = live_price

    db.commit()
    db.refresh(holding)

    investment = holding.buy_price * holding.quantity
    current_value = holding.current_price * holding.quantity
    profit_loss = current_value - investment

    return {
        "message": "Live price updated successfully",
        "symbol": holding.symbol,
        "buy_price": holding.buy_price,
        "current_price": holding.current_price,
        "quantity": holding.quantity,
        "investment": round(investment, 2),
        "current_value": round(current_value, 2),
        "profit_loss": round(profit_loss, 2)
    }