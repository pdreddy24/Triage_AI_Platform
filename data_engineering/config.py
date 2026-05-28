import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARTIFACTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "artifacts")

SCORING_LOG_PATH = os.path.join(ARTIFACTS_DIR, "scoring_logs.parquet")
EMBEDDING_PATH = os.path.join(ARTIFACTS_DIR, "embeddings", "latest.parquet")
GRAPH_PATH = os.path.join(ARTIFACTS_DIR, "graph", "latest.pkl")