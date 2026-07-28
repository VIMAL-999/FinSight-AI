from fastapi import APIRouter, HTTPException

from backend.services.stock_service import get_stock_price

router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


# -------------------------
# Live Stock Information
# -------------------------
@router.get("/{symbol}")
def stock_price(symbol: str):

    try:

        stock = get_stock_price(symbol)

        if stock["current_price"] is None:
            raise HTTPException(
                status_code=404,
                detail="Stock symbol not found"
            )

        return stock

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch market data"
        )