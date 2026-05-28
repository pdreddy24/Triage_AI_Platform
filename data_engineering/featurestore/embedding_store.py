import pandas as pd
from data_engineering.config import EMBEDDING_PATH


class EmbeddingStore:

    def __init__(self):
        self.df = None

    def load(self):
        self.df = pd.read_parquet(EMBEDDING_PATH)

    def get(self, node_id: str):
        row = self.df[self.df["node_id"] == node_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()