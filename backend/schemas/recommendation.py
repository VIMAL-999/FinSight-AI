from pydantic import BaseModel
from typing import List


class RecommendationResponse(BaseModel):
    symbol: str
    recommendation: str
    confidence: int
    risk: str
    reason: List[str]