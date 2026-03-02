import pandas as pd
import os
from data_engineering.config import SCORING_LOG_PATH


class ScoringLogStore:

    def __init__(self):
        os.makedirs(os.path.dirname(SCORING_LOG_PATH), exist_ok=True)

    def log(self, record: dict):
        df = pd.DataFrame([record])

        if os.path.exists(SCORING_LOG_PATH):
            existing = pd.read_parquet(SCORING_LOG_PATH)
            df = pd.concat([existing, df], ignore_index=True)

        df.to_parquet(SCORING_LOG_PATH, index=False)

    def load_all(self):
        if not os.path.exists(SCORING_LOG_PATH):
            return pd.DataFrame()
        return pd.read_parquet(SCORING_LOG_PATH)