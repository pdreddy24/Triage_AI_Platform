import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Default local embedding path (for dev)
LOCAL_DEFAULT_PATH = BASE_DIR.parent / "Training_service" / "artifacts" / "embeddings"

# Auto-pick newest parquet file if exists
def get_latest_embedding_file():
    if not LOCAL_DEFAULT_PATH.exists():
        return None

    parquet_files = list(LOCAL_DEFAULT_PATH.glob("embeddings_*.parquet"))
    if not parquet_files:
        return None

    # Pick newest file
    parquet_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return str(parquet_files[0])

EMBEDDING_PATH = os.getenv("EMBEDDING_PATH") or get_latest_embedding_file()

REFRESH_INTERVAL_SECONDS = int(os.getenv("REFRESH_INTERVAL_SECONDS", "300"))
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8001"))