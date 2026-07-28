from pydantic import BaseModel


class PortfolioSummary(BaseModel):
    portfolio_name: str
    total_investment: float
    current_value: float
    profit_loss: float
    return_percentage: float