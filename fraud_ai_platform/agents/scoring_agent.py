# agents/scoring_agent.py

import random
from .base_agent import BaseAgent


class ScoringAgent(BaseAgent):

    async def run(self, context: dict) -> dict:
        transaction = context["transaction"]

        # Simulated model logic
        risk_score = min(
            1.0,
            transaction["amount"] / 10000 + random.uniform(0, 0.2)
        )

        context["scoring"] = {
            "risk_score": round(risk_score, 4)
        }

        return context