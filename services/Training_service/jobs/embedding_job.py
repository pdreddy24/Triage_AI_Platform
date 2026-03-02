from pipelines.gnn_pipeline import export_embeddings
from config.paths import ARTIFACT_DIR
import os
import logging


def run_embedding_job(run_id: str,
                      gnn_model_path: str,
                      mapping_path: str):

    logging.info("Running embedding export job...")

    output_path = os.path.join(
        ARTIFACT_DIR,
        "embeddings",
        f"embeddings_{run_id}.parquet"
    )

    export_embeddings(
        gnn_model_path,
        mapping_path,
        output_path
    )

    logging.info(f"Embeddings saved at {output_path}")

    return output_path