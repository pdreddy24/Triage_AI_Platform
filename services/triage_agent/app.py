# services/triage_agent/app.py

from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import asyncio

app = FastAPI(title="AI Fraud Triage Agent")

SCORING_URL = "http://scoring-service:8001/score"
GRAPH_URL = "http://graph-service:8002/analyze"


class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    merchant: str


async def call_scoring(tx):
    async with httpx.AsyncClient() as client:
        res = await client.post(SCORING_URL, json=tx)
        return res.json()


async def call_graph(tx):
    async with httpx.AsyncClient() as client:
        res = await client.post(GRAPH_URL, json=tx)
        return res.json()


def decision_logic(score, graph):
    risk_score = score["risk_score"]
    graph_risk = graph["graph_risk"]

    combined = (risk_score * 0.6) + (graph_risk * 0.4)

    if combined > 0.8:
        action = "BLOCK"
    elif combined > 0.5:
        action = "REVIEW"
    else:
        action = "APPROVE"

    explanation = f"""
    Model Risk: {risk_score}
    Graph Risk: {graph_risk}
    Combined Risk: {round(combined, 4)}
    """

    return combined, action, explanation


@app.post("/triage")
async def triage(tx: Transaction):

    scoring_task = call_scoring(tx.dict())
    graph_task = call_graph(tx.dict())

    score, graph = await asyncio.gather(scoring_task, graph_task)

    combined, action, explanation = decision_logic(score, graph)

    return {
        "transaction_id": tx.transaction_id,
        "risk_score": score["risk_score"],
        "graph_risk": graph["graph_risk"],
        "combined_risk": round(combined, 4),
        "decision": action,
        "explanation": explanation
    }