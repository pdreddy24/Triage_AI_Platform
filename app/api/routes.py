from fastapi import APIRouter, HTTPException
from api.schemas import TransactionRequest, ScoreResponse
from api.client import call_scoring_service

router = APIRouter(prefix="/api", tags=["Fraud API"])


@router.post("/score", response_model=ScoreResponse)
def score(tx: TransactionRequest):
    try:
        result = call_scoring_service(tx.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))