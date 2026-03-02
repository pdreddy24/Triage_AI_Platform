from pydantic import BaseModel
from typing import Dict


class EmbeddingResponse(BaseModel):
    user_id: int
    embedding: Dict[str, float]


class HealthResponse(BaseModel):
    status: str