from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Read and update the shared workflow context."""
