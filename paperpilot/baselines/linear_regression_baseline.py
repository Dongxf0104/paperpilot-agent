from __future__ import annotations

from typing import Sequence

from paperpilot.baselines.adapters import BaseBaselineAdapter


def _solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            augmented[pivot][col] = 1e-12
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            factor = augmented[row][col]
            augmented[row] = [
                current - factor * pivot_value
                for current, pivot_value in zip(augmented[row], augmented[col])
            ]
    return [row[-1] for row in augmented]


class LinearRegressionBaseline(BaseBaselineAdapter):
    def fit(self, X: Sequence[Sequence[float]], y: Sequence[float]) -> "LinearRegressionBaseline":
        if not X or not y:
            raise ValueError("Cannot fit LinearRegressionBaseline with empty data.")
        design = [[1.0] + [float(value) for value in row] for row in X]
        width = len(design[0])
        xtx = [[0.0 for _ in range(width)] for _ in range(width)]
        xty = [0.0 for _ in range(width)]
        for row, target in zip(design, y):
            for i in range(width):
                xty[i] += row[i] * float(target)
                for j in range(width):
                    xtx[i][j] += row[i] * row[j]

        ridge = float(self.config.get("ridge", 1e-8))
        for i in range(width):
            xtx[i][i] += ridge
        self.coef_ = _solve_linear_system(xtx, xty)
        return self

    def predict(self, X: Sequence[Sequence[float]]) -> list[float]:
        if not hasattr(self, "coef_"):
            raise RuntimeError("LinearRegressionBaseline must be fit before predict.")
        predictions = []
        for row in X:
            values = [1.0] + [float(value) for value in row]
            predictions.append(sum(weight * value for weight, value in zip(self.coef_, values)))
        return predictions
