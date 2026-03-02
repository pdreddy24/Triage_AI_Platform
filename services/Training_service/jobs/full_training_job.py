# training_service/jobs/full_training_job.py

import logging
from datetime import datetime, timezone

from jobs.dataset_job import run_dataset_job
from jobs.graph_job import run_graph_job
from jobs.gnn_training_job import run_gnn_training_job
from jobs.embedding_job import run_embedding_job
from jobs.gbt_training_job import run_gbt_training_job
from jobs.calibration_job import run_calibration_job

logging.basicConfig(level=logging.INFO)


def run_full_training():

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    logging.info(f"Starting full training pipeline | run_id={run_id}")

    dataset_path = run_dataset_job(run_id)

    graph_path, mapping_path = run_graph_job(run_id, dataset_path)

    gnn_model_path = run_gnn_training_job(run_id, graph_path)

    # ✅ FIXED: pass mapping_path instead of graph_path
    embedding_path = run_embedding_job(run_id, gnn_model_path, mapping_path)

    gbt_model_path = run_gbt_training_job(run_id, dataset_path, embedding_path)

    run_calibration_job(
    run_id,
    gbt_model_path,
    dataset_path,
    embedding_path
)

    logging.info(f"Training pipeline completed successfully | run_id={run_id}")


if __name__ == "__main__":
    run_full_training()