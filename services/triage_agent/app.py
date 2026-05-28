import asyncio
import os
from typing import Any, Dict

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="AI Fraud Triage Agent")

SCORING_URL = os.getenv("SCORING_URL", "http://scoring-service:8001/score")
GRAPH_URL = os.getenv("GRAPH_URL", "http://graph-service:8002/analyze")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))


class Transaction(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    amount: float = Field(..., ge=0)
    merchant: str = Field(..., min_length=1)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "triage-agent ok"}


async def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Dependency returned an error from {url}: {exc.response.text}",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not reach dependency {url}: {str(exc)}",
        ) from exc


async def call_scoring(tx: Dict[str, Any]) -> Dict[str, Any]:
    return await post_json(SCORING_URL, tx)


async def call_graph(tx: Dict[str, Any]) -> Dict[str, Any]:
    return await post_json(GRAPH_URL, tx)


def decision_logic(score: Dict[str, Any], graph: Dict[str, Any]):
    try:
        risk_score = float(score["risk_score"])
        graph_risk = float(graph["graph_risk"])
    except KeyError as exc:
        raise HTTPException(status_code=502, detail=f"Dependency response missing key: {exc}") from exc

    combined = (risk_score * 0.6) + (graph_risk * 0.4)

    if combined > 0.8:
        action = "BLOCK"
    elif combined > 0.5:
        action = "REVIEW"
    else:
        action = "APPROVE"

    explanation = (
        f"Model Risk: {risk_score}\n"
        f"Graph Risk: {graph_risk}\n"
        f"Combined Risk: {round(combined, 4)}"
    )

    return combined, action, explanation


@app.post("/triage")
async def triage(tx: Transaction):
    payload = tx.model_dump()

    score, graph = await asyncio.gather(
        call_scoring(payload),
        call_graph(payload),
    )

    combined, action, explanation = decision_logic(score, graph)

    return {
        "transaction_id": tx.transaction_id,
        "risk_score": score["risk_score"],
        "graph_risk": graph["graph_risk"],
        "combined_risk": round(combined, 4),
        "decision": action,
        "explanation": explanation,
        "scoring_details": score,
        "graph_details": graph,
    }
