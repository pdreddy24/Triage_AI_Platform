# services/fraud_api/schemas.py

from pydantic import BaseModel, Field

class TransactionSchema(BaseModel):
    transaction_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    merchant: str = Field(min_length=1)