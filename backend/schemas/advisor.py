from pydantic import BaseModel


class AdvisorResponse(BaseModel):
    portfolio_health: str
    risk_level: str
    diversification_score: int
    best_performer: str
    worst_performer: str
    recommendation: str