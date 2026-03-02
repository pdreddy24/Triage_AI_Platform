# training_service/pipelines/gnn_pipeline.py

import pickle
import torch
import numpy as np
import pandas as pd

from core.graph.gnn_converter import convert_to_pyg


def train_gnn(graph_path: str, output_path: str):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    data = convert_to_pyg(G)

    # Dummy model state (replace with real GNN later)
    model_state = {"num_nodes": data.num_nodes}
    torch.save(model_state, output_path)


def export_embeddings(gnn_model_path: str, graph_path: str, output_path: str):
    with open(graph_path, "rb") as f:
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
    df.to_parquet(output_path)