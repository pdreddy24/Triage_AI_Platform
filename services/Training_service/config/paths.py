# training_service/config/paths.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

DATASET_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "dataset")
GRAPH_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "graph")
GNN_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "gnn")
EMBEDDING_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "embeddings")
GBT_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "gbt")
METADATA_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, "metadata")

for path in [
    DATASET_ARTIFACT_DIR,
    GRAPH_ARTIFACT_DIR,
    GNN_ARTIFACT_DIR,
    EMBEDDING_ARTIFACT_DIR,
    GBT_ARTIFACT_DIR,
    METADATA_ARTIFACT_DIR,
]:
    os.makedirs(path, exist_ok=True)