# services/graph_service/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import random
import time
from collections import deque

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

app = FastAPI(title="Graph Service - Enterprise Production")

# ==========================================================
# METRICS
# ==========================================================

# Traffic
REQUEST_COUNT = Counter(
    "graph_requests_total",
    "Total graph analysis requests"
)

ERROR_COUNT = Counter(
    "graph_errors_total",
    "Total graph analysis errors"
)

INFLIGHT_REQUESTS = Gauge(
    "graph_inflight_requests",
    "Number of in-flight graph requests"
)

# Latency
LATENCY = Histogram(
    "graph_latency_seconds",
    "Graph endpoint latency",
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5)
)

DEPTH_LATENCY = Histogram(
    "graph_depth_latency_seconds",
    "Graph traversal depth latency",
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2)
)

DEPENDENCY_LATENCY = Histogram(
    "graph_dependency_latency_seconds",
    "Graph external dependency latency",
    buckets=(0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5)
)

# Risk / anomaly
ANOMALY_RATIO = Gauge(
    "graph_high_risk_ratio",
    "Ratio of high-risk graph detections"
)

# Circuit breaker
CIRCUIT_STATE = Gauge(
    "graph_circuit_state",
    "1 = open, 0 = closed"
)

# SLO
SLO_BREACH_COUNT = Counter(
    "graph_slo_breach_total",
    "Total graph latency SLO breaches"
)

Instrumentator().instrument(app).expose(app)

# ==========================================================
# CONFIGURATION
# ==========================================================

SLO_THRESHOLD_SECONDS = 0.5
HIGH_RISK_THRESHOLD = 0.75
ERROR_THRESHOLD = 5
WINDOW_SIZE = 20
REQUEST_TIMEOUT = 0.6
MAX_RETRIES = 2

error_window = deque(maxlen=WINDOW_SIZE)
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
    return {"status": "graph-service ok"}


# ==========================================================
# HELPER: CIRCUIT CHECK
# ==========================================================

def is_circuit_open():
    if len(error_window) < ERROR_THRESHOLD:
        return False
    return sum(error_window) >= ERROR_THRESHOLD


# ==========================================================
# GRAPH ANALYSIS
# ==========================================================

@app.post("/analyze")
async def analyze(tx: Transaction):

    global total_requests, high_risk_count

    if is_circuit_open():
        CIRCUIT_STATE.set(1)
        raise HTTPException(status_code=503, detail="Circuit open")

    CIRCUIT_STATE.set(0)
    INFLIGHT_REQUESTS.inc()
    REQUEST_COUNT.inc()
    total_requests += 1

    start_time = time.time()

    try:
        # --------------------------------------------------
        # 1️⃣ Graph Depth Traversal Simulation
        # --------------------------------------------------
        depth_start = time.time()

        graph_depth = random.randint(1, 6)

        await asyncio.wait_for(
            asyncio.sleep(graph_depth * random.uniform(0.01, 0.05)),
            timeout=REQUEST_TIMEOUT
        )

        DEPTH_LATENCY.observe(time.time() - depth_start)

        # --------------------------------------------------
        # 2️⃣ External Dependency Simulation (DB/Neo4j)
        # --------------------------------------------------
        dep_start = time.time()

        retry = 0
        while retry <= MAX_RETRIES:
            try:
                await asyncio.wait_for(
                    asyncio.sleep(random.uniform(0.01, 0.05)),
                    timeout=REQUEST_TIMEOUT
                )
                break
            except asyncio.TimeoutError:
                retry += 1
                if retry > MAX_RETRIES:
                    raise

        DEPENDENCY_LATENCY.observe(time.time() - dep_start)

        # --------------------------------------------------
        # 3️⃣ Risk Calculation
        # --------------------------------------------------
        connected_accounts = random.randint(1, 5)
        suspicious_edges = random.randint(0, 3)

        graph_risk = min(
            1.0,
            (connected_accounts * 0.1)
            + (suspicious_edges * 0.2)
            + random.uniform(0, 0.2)
        )

        if graph_risk > HIGH_RISK_THRESHOLD:
            high_risk_count += 1

        if total_requests > 0:
            ANOMALY_RATIO.set(high_risk_count / total_requests)

        error_window.append(0)

        return {
            "transaction_id": tx.transaction_id,
            "graph_depth": graph_depth,
            "connected_accounts": connected_accounts,
            "suspicious_edges": suspicious_edges,
            "graph_risk": round(graph_risk, 4),
            "high_risk": graph_risk > HIGH_RISK_THRESHOLD
        }

    except Exception:
        ERROR_COUNT.inc()
        error_window.append(1)
        raise HTTPException(status_code=500, detail="Graph processing failed")

    finally:
        total_latency = time.time() - start_time
        LATENCY.observe(total_latency)

        if total_latency > SLO_THRESHOLD_SECONDS:
            SLO_BREACH_COUNT.inc()

        INFLIGHT_REQUESTS.dec()