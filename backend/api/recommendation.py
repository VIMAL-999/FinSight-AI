from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import Holding

from backend.schemas.recommendation import (
    RecommendationResponse
)

from backend.services.recommendation_service import (
    generate_recommendation
)

router = APIRouter(
    prefix="/recommendation",
    tags=["AI Recommendation"]
)


@router.get(
    "/{holding_id}",
    response_model=RecommendationResponse
)
def recommend_stock(
    holding_id: int,
    db: Session = Depends(get_db)
):

    holding = db.query(
        Holding
    ).filter(
        Holding.id == holding_id
    ).first()

    if holding is None:

        raise HTTPException(
            status_code=404,
            detail="Holding not found"
        )

    result = generate_recommendation(
        holding.buy_price,
        holding.current_price,
        holding.quantity
    )

    return {

        "symbol": holding.symbol,

        "recommendation":
        result["recommendation"],

        "confidence":
        result["confidence"],

        "risk":
        result["risk"],

        "reason":
        result["reason"]
    }