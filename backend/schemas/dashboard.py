from pydantic import BaseModel
from typing import Dict


class DashboardResponse(BaseModel):
    investment_score: int
    total_holdings: int
    top_gainer: str
    top_loser: str
    allocation: Dict[str, float]
    warning: str