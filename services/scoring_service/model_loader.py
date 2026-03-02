import joblib
import logging
import pandas as pd
from core.config.model_config import MODEL_PATH

logger = logging.getLogger(__name__)

model = None

FEATURE_NAMES = ["amount", "velocity_1h", "emb_0", "emb_1", "emb_2", "emb_3"]


def load_model():
    global model
    if not MODEL_PATH:
        raise RuntimeError("MODEL_PATH not set")

    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded from {MODEL_PATH}")


def predict_proba(features):
    if model is None:
        raise RuntimeError("Model not loaded")

    df = pd.DataFrame([features], columns=FEATURE_NAMES)
    return float(model.predict_proba(df)[0][1])