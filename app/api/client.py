import requests
from core.config.service_config import SCORING_SERVICE_URL


def call_scoring_service(payload: dict):
    response = requests.post(
        f"{SCORING_SERVICE_URL}/score",
        json=payload,
        timeout=5
    )

    if response.status_code != 200:
        raise RuntimeError(f"Scoring service error: {response.text}")

    return response.json()