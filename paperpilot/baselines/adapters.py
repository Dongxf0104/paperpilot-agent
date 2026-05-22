from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from paperpilot.metrics.registry import compute_metrics


class BaseBaselineAdapter(ABC):
    def __init__(self, config: dict | None = None) -> None:
        self.config = config or {}

    @abstractmethod
    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "BaseBaselineAdapter":
        """Fit the baseline."""

    @abstractmethod
    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        """Predict target values."""

    def evaluate(self, X: Sequence[Sequence[float]], y: Sequence[float], metrics: Sequence[str]) -> dict[str, float]:
        predictions = self.predict(X)
        return compute_metrics(y, predictions, metrics)
