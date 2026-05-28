# core/graph/schema.py

from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_id: str
    user_id: str
    device_id: str
    amount: float
    timestamp: int