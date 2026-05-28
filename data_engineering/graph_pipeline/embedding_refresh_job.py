import pickle
import numpy as np
import pandas as pd
from data_engineering.config import GRAPH_PATH, EMBEDDING_PATH


def refresh_embeddings():
    with open(GRAPH_PATH, "rb") as f:
        G = pickle.load(f)

    embeddings = []

    for node in G.nodes:
        embeddings.append({
            "node_id": node,
            "emb_0": np.random.randn(),
            "emb_1": np.random.randn(),
            "emb_2": np.random.randn(),
            "emb_3": np.random.randn(),
        })

    df = pd.DataFrame(embeddings)
    df.to_parquet(EMBEDDING_PATH, index=False)

    print("Embeddings refreshed.")