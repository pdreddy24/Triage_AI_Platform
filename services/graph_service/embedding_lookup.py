import pandas as pd
import os
import threading
import time
from config import EMBEDDING_PATH, REFRESH_INTERVAL_SECONDS


class EmbeddingStore:
    def __init__(self):
        self.embedding_df = None
        self.lock = threading.Lock()
        self.last_loaded = None

    def load_embeddings(self):
        if not os.path.exists(EMBEDDING_PATH):
            raise FileNotFoundError(f"Embedding file not found: {EMBEDDING_PATH}")

        df = pd.read_parquet(EMBEDDING_PATH)

        if "user_id" not in df.columns:
            raise ValueError("Embeddings must contain user_id column")

        with self.lock:
            self.embedding_df = df
            self.last_loaded = time.time()

    def get_embedding(self, user_id: int):
        with self.lock:
            if self.embedding_df is None:
                return None

            row = self.embedding_df[self.embedding_df["user_id"] == user_id]
            if row.empty:
                return None

            row_dict = row.to_dict(orient="records")[0]

            embedding = {
                k: v for k, v in row_dict.items()
                if k.startswith("emb_")
            }

            return embedding

    def auto_refresh_loop(self):
        while True:
            try:
                self.load_embeddings()
            except Exception as e:
                print(f"[Embedding Refresh Error] {e}")
            time.sleep(REFRESH_INTERVAL_SECONDS)


# 👇 THIS LINE MUST EXIST
embedding_store = EmbeddingStore()