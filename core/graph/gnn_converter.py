# core/graph/gnn_converter.py

import torch
from torch_geometric.utils import from_networkx


def convert_to_pyg(graph):
    data = from_networkx(graph)

    # Placeholder node features (can be replaced later)
    num_nodes = graph.number_of_nodes()
    data.x = torch.ones((num_nodes, 8))

    return data