from pydantic import BaseModel, Field
from datetime import datetime


class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: int = Field(..., gt=0)
    device_id: int = Field(..., gt=0)
    merchant_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    timestamp: datetime


class ScoreResponse(BaseModel):
    transaction_id: str
    timestamp: datetime
    risk_score: float = Field(..., ge=0, le=1)
    risk_band: str
    decision: str
    route_to: str
    model_version: str