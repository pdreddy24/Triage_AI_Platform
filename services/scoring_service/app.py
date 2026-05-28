# services/scoring_service/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import asyncio
import time

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

app = FastAPI(title="Scoring Service - Enterprise Production")

# ==========================================================
# METRICS
# ==========================================================

# Traffic
REQUEST_COUNT = Counter(
    "score_requests_total",
    "Total scoring requests"
)

ERROR_COUNT = Counter(
    "score_errors_total",
    "Total scoring errors"
)

# Latency
LATENCY = Histogram(
    "score_latency_seconds",
    "Scoring endpoint latency",
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5)
)

# Dependency latency (model/db call simulation)
DEPENDENCY_LATENCY = Histogram(
    "score_dependency_latency_seconds",
    "Scoring dependency latency",
    buckets=(0.005, 0.01, 0.02, 0.05, 0.1, 0.2)
)

# High-risk anomaly ratio
ANOMALY_GAUGE = Gauge(
    "score_high_risk_ratio",
    "High risk scoring ratio"
)

# Circuit breaker state
CIRCUIT_STATE = Gauge(
    "score_circuit_state",
    "1 = open, 0 = closed"
)

# SLO breach counter
SLO_BREACH_COUNT = Counter(
    "score_slo_breach_total",
    "Total SLO latency breaches"
)

Instrumentator().instrument(app).expose(app)

# ==========================================================
# CONFIG
# ==========================================================

SLO_THRESHOLD_SECONDS = 0.3
HIGH_RISK_THRESHOLD = 0.75
ERROR_THRESHOLD = 5
REQUEST_TIMEOUT = 0.5

error_window = 0
total_requests = 0
high_risk_count = 0


# ==========================================================
# MODEL
# ==========================================================

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    merchant: str


# ==========================================================
# HEALTH
# ==========================================================

@app.get("/health")
async def health():
    return {"status": "scoring-service ok"}


# ==========================================================
# SCORING ENDPOINT
# ==========================================================

@app.post("/score")
async def score(tx: Transaction):

    global error_window, total_requests, high_risk_count

    if CIRCUIT_STATE._value.get() == 1:
        raise HTTPException(status_code=503, detail="Circuit open")

    REQUEST_COUNT.inc()
    total_requests += 1

    start_time = time.time()

    try:
        # ------------------------------------------------------
        # 1️⃣ Simulated Dependency (Model / DB Call)
        # ------------------------------------------------------
        dep_start = time.time()

        await asyncio.wait_for(
            asyncio.sleep(random.uniform(0.01, 0.05)),
            timeout=REQUEST_TIMEOUT
        )

        DEPENDENCY_LATENCY.observe(time.time() - dep_start)

        # ------------------------------------------------------
        # 2️⃣ Risk Computation
        # ------------------------------------------------------
        risk = min(
            1.0,
            tx.amount / 10000 + random.random() * 0.2
        )

        # Track anomaly ratio
        if risk > HIGH_RISK_THRESHOLD:
            high_risk_count += 1

        if total_requests > 0:
            ANOMALY_GAUGE.set(high_risk_count / total_requests)

        # Reset circuit if healthy
        error_window = 0
        CIRCUIT_STATE.set(0)

        return {
            "transaction_id": tx.transaction_id,
            "risk_score": round(risk, 4),
            "high_risk": risk > HIGH_RISK_THRESHOLD
        }

    except asyncio.TimeoutError:
        ERROR_COUNT.inc()
        error_window += 1

        if error_window >= ERROR_THRESHOLD:
            CIRCUIT_STATE.set(1)

        raise HTTPException(status_code=504, detail="Scoring timeout")

    except Exception:
        ERROR_COUNT.inc()
        error_window += 1

        if error_window >= ERROR_THRESHOLD:
            CIRCUIT_STATE.set(1)

        raise HTTPException(status_code=500, detail="Scoring error")

    finally:
        total_latency = time.time() - start_time
        LATENCY.observe(total_latency)

        # ------------------------------------------------------
        # 3️⃣ SLO Monitoring
        # ------------------------------------------------------
        if total_latency > SLO_THRESHOLD_SECONDS:
            SLO_BREACH_COUNT.inc()