# triage_api.py

from fastapi import FastAPI
from pydantic import BaseModel

from agents.orchestrator import OrchestratorAgent

app = FastAPI(title="Research-Grade Fraud Agent Platform")

orchestrator = OrchestratorAgent()


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    merchant: str


@app.get("/")
async def root():
    return {"message": "Fraud AI Agent Platform Running"}


@app.post("/triage")
async def triage(tx: Transaction):

    result = await orchestrator.run(tx.dict())

    return result