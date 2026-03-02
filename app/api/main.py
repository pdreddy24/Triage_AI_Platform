# app/api/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import httpx
import io
import asyncio
import time
from typing import List

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Fraud AI Triage API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)

SCORING_URL = "http://scoring-service:8001/score"
GRAPH_URL = "http://graph-service:8002/graph"

REQUIRED_COLUMNS = {"user_id", "amount", "location"}


@app.get("/health")
def health():
    return {"status": "ok"}


async def process_row(client: httpx.AsyncClient, payload: dict):
    """Process single row: scoring + graph"""

    score_data = {}
    graph_data = {}

    try:
        score_response = await client.post(SCORING_URL, json=payload)
        score_response.raise_for_status()
        score_data = score_response.json()
    except Exception as e:
        score_data = {"error": str(e)}

    try:
        graph_response = await client.post(GRAPH_URL, json=payload)
        graph_response.raise_for_status()
        graph_data = graph_response.json()
    except Exception as e:
        graph_data = {"error": str(e)}

    return {
        "input": payload,
        "score": score_data,
        "graph": graph_data,
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    start_time = time.time()

    # 1️⃣ File validation
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    # 2️⃣ Parse CSV
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV has no rows")

    # 3️⃣ Schema validation
    if not REQUIRED_COLUMNS.issubset(set(df.columns)):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {REQUIRED_COLUMNS}",
        )

    # 4️⃣ Convert rows to dict
    records = df.to_dict(orient="records")

    # 5️⃣ Async parallel processing
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [process_row(client, record) for record in records]
        results = await asyncio.gather(*tasks)

    total_latency = round(time.time() - start_time, 4)

    return {
        "processed_records": len(results),
        "total_latency_seconds": total_latency,
        "results": results,
    }