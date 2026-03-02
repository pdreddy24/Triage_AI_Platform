# training_service/jobs/gnn_training_job.py

import logging
from pipelines.gnn_pipeline import train_gnn
from config.paths import GNN_ARTIFACT_DIR


def run_gnn_training_job(run_id: str, graph_path: str) -> str:
    logging.info("Running GNN training job...")
    output_path = f"{GNN_ARTIFACT_DIR}/gnn_{run_id}.pt"
    train_gnn(graph_path, output_path)
    logging.info(f"GNN model saved at {output_path}")
    return output_path