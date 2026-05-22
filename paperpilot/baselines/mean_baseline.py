from __future__ import annotations

from typing import Sequence

from paperpilot.baselines.adapters import BaseBaselineAdapter


class MeanBaseline(BaseBaselineAdapter):
    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "MeanBaseline":
        if not y:
            raise ValueError("Cannot fit MeanBaseline with empty y.")
        self.mean_ = sum(float(value) for value in y) / len(y)
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        if not hasattr(self, "mean_"):
            raise RuntimeError("MeanBaseline must be fit before predict.")
        return [self.mean_ for _ in X]
