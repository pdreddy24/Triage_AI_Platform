# core/graph/fraud_graph.py

import networkx as nx
from typing import List
from core.graph.schema import Transaction


class FraudGraph:

    def __init__(self):
        self.graph = nx.Graph()

    def add_transaction(self, txn: Transaction):
        user_node = f"user_{txn.user_id}"
        device_node = f"device_{txn.device_id}"

        self.graph.add_node(user_node, node_type="user")
        self.graph.add_node(device_node, node_type="device")

        self.graph.add_edge(user_node, device_node)

    def build_from_transactions(self, transactions: List[Transaction]):
        for txn in transactions:
            self.add_transaction(txn)

    def get_graph(self):
        return self.graph