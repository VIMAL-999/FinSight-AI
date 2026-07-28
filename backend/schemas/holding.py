from pydantic import BaseModel


class HoldingCreate(BaseModel):
    portfolio_id: int
    symbol: str
    company_name: str
    quantity: float
    buy_price: float
    current_price: float


class HoldingResponse(BaseModel):
    id: int
    portfolio_id: int
    symbol: str
    company_name: str
    quantity: float
    buy_price: float
    current_price: float

    class Config:
        from_attributes = True