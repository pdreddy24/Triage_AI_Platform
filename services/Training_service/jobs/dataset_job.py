# training_service/jobs/dataset_job.py

import logging
from pipelines.dataset_builder import build_training_dataset
from config.paths import DATASET_ARTIFACT_DIR


def run_dataset_job(run_id: str) -> str:
    logging.info("Running dataset job...")
    output_path = f"{DATASET_ARTIFACT_DIR}/dataset_{run_id}.parquet"
    build_training_dataset(output_path)
    logging.info(f"Dataset created at {output_path}")
    return output_path