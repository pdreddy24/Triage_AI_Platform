import os

GRAPH_SERVICE_URL = os.getenv("GRAPH_SERVICE_URL", "http://127.0.0.1:8000")
SCORING_SERVICE_URL = os.getenv("SCORING_SERVICE_URL", "http://localhost:8002")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://127.0.0.1:9000")
