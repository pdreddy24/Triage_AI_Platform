import requests
import logging
import numpy as np

from core.config.service_config import GRAPH_SERVICE_URL
from core.features.velocity_store import update_velocity

logger = logging.getLogger(__name__)

# Reuse connection pool (better performance)
session = requests.Session()


def get_embedding(user_id: int):
    """
    Fetch user embedding from graph service.
    If graph is slow or unavailable, fallback to zero embedding.
    """

    url = f"{GRAPH_SERVICE_URL}/embedding/{user_id}"

    try:
        # ✅ CRITICAL FIX: Add timeout
        response = session.get(url, timeout=1.5)

        if response.status_code != 200:
            logger.warning(
                f"Graph returned {response.status_code} for user {user_id}. Using fallback embedding."
            )
            return [0.0, 0.0, 0.0, 0.0]

        embedding = response.json().get("embedding")

        if not embedding:
            return [0.0, 0.0, 0.0, 0.0]

        # Ensure exactly 4 dimensions
        embedding = (embedding + [0.0, 0.0, 0.0, 0.0])[:4]

        return embedding

    except requests.exceptions.Timeout:
        logger.warning(f"Graph timeout for user {user_id}. Using fallback embedding.")
        return [0.0, 0.0, 0.0, 0.0]

    except requests.exceptions.RequestException as e:
        logger.error(f"Graph service error: {e}")
        return [0.0, 0.0, 0.0, 0.0]


def build_features(tx: dict):
    """
    Build model-ready feature vector.
    Always returns immediately even if graph fails.
    """

    # External dependency (safe now due to timeout)
    embedding = get_embedding(tx["user_id"])

    # Internal store
    velocity = update_velocity(tx["user_id"])

    features = {
        "amount": tx["amount"],
        "velocity_1h": velocity,
        "emb_0": embedding[0],
        "emb_1": embedding[1],
        "emb_2": embedding[2],
        "emb_3": embedding[3],
    }

    # LightGBM strict order
    ordered_features = [
        features["amount"],
        features["velocity_1h"],
        features["emb_0"],
        features["emb_1"],
        features["emb_2"],
        features["emb_3"],
    ]

    return ordered_features, features, velocity