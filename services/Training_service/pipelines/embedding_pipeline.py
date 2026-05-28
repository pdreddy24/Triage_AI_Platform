# training_service/pipelines/embedding_pipeline.py

import torch
import pandas as pd
import pickle


def export_user_embeddings(gnn_model_path: str,
                           mapping_path: str,
                           output_path: str):

    # Load GNN model
    model = torch.load(gnn_model_path)
    model.eval()

    # Extract embedding matrix
    with torch.no_grad():
        embeddings = model.embeddings.weight.cpu().numpy()

    # Load node mapping
    with open(mapping_path, "rb") as f:
        node_mapping = pickle.load(f)

    # Create DataFrame
    emb_df = pd.DataFrame(
        embeddings,
        columns=[f"emb_{i}" for i in range(embeddings.shape[1])]
    )

    # Map node index → user_id
    emb_df["user_id"] = [
        node_mapping[i] for i in range(len(emb_df))
    ]

    emb_df.to_parquet(output_path)