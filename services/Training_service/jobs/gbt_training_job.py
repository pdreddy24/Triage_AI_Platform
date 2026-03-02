# training_service/jobs/gbt_training_job.py

import logging
from pipelines.gbt_pipeline import train_gbt
from config.paths import GBT_ARTIFACT_DIR


def run_gbt_training_job(run_id: str, dataset_path: str, embedding_path: str) -> str:
    logging.info("Running GBT training job...")
    output_path = f"{GBT_ARTIFACT_DIR}/gbt_{run_id}.pkl"
    train_gbt(dataset_path, embedding_path, output_path)
    logging.info(f"GBT model saved at {output_path}")
    return output_path