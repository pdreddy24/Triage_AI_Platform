# agents/policy_agent.py

from .base_agent import BaseAgent


class PolicyAgent(BaseAgent):

    async def run(self, context: dict) -> dict:

        score = context["scoring"]["risk_score"]
        graph = context["graph"]["graph_risk"]

        combined = (score * 0.6) + (graph * 0.4)

        if combined > 0.8:
            decision = "BLOCK"
        elif combined > 0.5:
            decision = "REVIEW"
        else:
            decision = "APPROVE"

        context["decision"] = {
            "combined_risk": round(combined, 4),
            "action": decision
        }

        return context