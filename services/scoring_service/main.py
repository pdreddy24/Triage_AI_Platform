from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from datetime import datetime, UTC
import random

app = FastAPI(title="Scoring Service")

Instrumentator().instrument(app).expose(app)

@app.post("/score")
async def score(payload: dict):
    return {
        "transaction_id": payload.get("transaction_id"),
        "timestamp": datetime.now(UTC),
        "risk_score": round(random.random(), 2),
        "decision": "APPROVE",
        "model_version": "1.0.0"
    }