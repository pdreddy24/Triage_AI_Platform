# training_service/pipelines/graph_pipeline.py

import pickle
import pandas as pd
from core.graph.fraud_graph import FraudGraph
from core.graph.schema import Transaction


def build_graph(dataset_path: str, output_path: str):
    df = pd.read_parquet(dataset_path)

    fraud_graph = FraudGraph()

    transactions = [
        Transaction(
            transaction_id=str(row.transaction_id),
            user_id=str(row.user_id),
            device_id=str(row.device_id),
            amount=float(row.amount),
            timestamp=int(row.timestamp)
        )
        for _, row in df.iterrows()
    ]

    fraud_graph.build_from_transactions(transactions)

    with open(output_path, "wb") as f:
        pickle.dump(fraud_graph.get_graph(), f)