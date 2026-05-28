# training_service/jobs/graph_job.py

import logging
import os
from pipelines.graph_pipeline import build_graph
from config.paths import GRAPH_ARTIFACT_DIR


def run_graph_job(run_id: str, dataset_path: str):

    logging.info("Running graph construction job...")

    graph_output_path = os.path.join(
        GRAPH_ARTIFACT_DIR,
        f"graph_{run_id}.pkl"
    )

    mapping_output_path = os.path.join(
        GRAPH_ARTIFACT_DIR,
        f"node_mapping_{run_id}.pkl"
    )

    graph_path, mapping_path = build_graph(
        dataset_path,
        graph_output_path,
        mapping_output_path
    )

    logging.info(f"Graph saved at {graph_path}")
    logging.info(f"Node mapping saved at {mapping_path}")

    return graph_path, mapping_path