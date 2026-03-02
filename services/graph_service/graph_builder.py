# graph_service/graph_builder.py

from core.graph.fraud_graph import FraudGraph
from core.graph.schema import Transaction


def build_graph_from_request(transactions_data):
    fraud_graph = FraudGraph()

    transactions = [
        Transaction(
            transaction_id=str(txn["transaction_id"]),
            user_id=str(txn["user_id"]),
            device_id=str(txn["device_id"]),
            amount=float(txn["amount"]),
            timestamp=int(txn["timestamp"])
        )
        for txn in transactions_data
    ]

    fraud_graph.build_from_transactions(transactions)

    return fraud_graph.get_graph()