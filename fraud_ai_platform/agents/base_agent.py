# agents/base_agent.py

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract agent definition.
    Every agent:
    - Receives context
    - Modifies context
    - Returns updated context
    """

    @abstractmethod
    async def run(self, context: dict) -> dict:
        pass