# agents/orchestrator.py

from .scoring_agent import ScoringAgent
from .graph_agent import GraphAgent
from .policy_agent import PolicyAgent


class OrchestratorAgent:

    def __init__(self):
        self.pipeline = [
            ScoringAgent(),
            GraphAgent(),
            PolicyAgent()
        ]

    async def run(self, transaction: dict) -> dict:

        context = {
            "transaction": transaction
        }

        for agent in self.pipeline:
            context = await agent.run(context)

        return context