import pickle
from core.graph.fraud_graph import FraudGraph
from core.graph.schema import Transaction


def build_graph(transactions, output_path):
    fraud_graph = FraudGraph()
    fraud_graph.build_from_transactions(transactions)

    with open(output_path, "wb") as f:
        pickle.dump(fraud_graph.get_graph(), f)