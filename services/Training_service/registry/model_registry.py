# training_service/registry/model_registry.py

import json
from config.paths import METADATA_ARTIFACT_DIR


def register_model(run_id: str, gbt_model_path: str, metrics: dict):
    metadata = {
        "run_id": run_id,
        "gbt_model_path": gbt_model_path,
        "metrics": metrics,
    }

    output_path = f"{METADATA_ARTIFACT_DIR}/model_{run_id}.json"

    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=2)