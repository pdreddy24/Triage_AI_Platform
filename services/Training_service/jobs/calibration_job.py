# training_service/jobs/calibration_job.py

import logging
from pipelines.calibration_pipeline import calibrate_model


def run_calibration_job(run_id: str,
                        gbt_model_path: str,
                        dataset_path: str,
                        embedding_path: str):

    logging.info("Running calibration job...")

    metrics = calibrate_model(
        gbt_model_path,
        dataset_path,
        embedding_path
    )

    logging.info(f"Calibration metrics: {metrics}")

    return metrics