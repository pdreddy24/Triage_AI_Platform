# agents/graph_agent.py

import random
from .base_agent import BaseAgent


class GraphAgent(BaseAgent):

    async def run(self, context: dict) -> dict:

        connected_accounts = random.randint(1, 5)
        suspicious_edges = random.randint(0, 3)

        graph_risk = min(
            1.0,
            connected_accounts * 0.1 +
            suspicious_edges * 0.2 +
            random.uniform(0, 0.2)
        )

        context["graph"] = {
            "connected_accounts": connected_accounts,
            "suspicious_edges": suspicious_edges,
            "graph_risk": round(graph_risk, 4)
        }

        return context