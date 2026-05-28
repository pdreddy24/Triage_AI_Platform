from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: int
    device_id: int
    merchant_id: int
    amount: float
    timestamp: datetime


class ScoreResponse(BaseModel):
    transaction_id: str
    timestamp: datetime
    risk_score: float
    decision: str
    velocity_1h: int
    features_used: Dict[str, float]
    model_version: str