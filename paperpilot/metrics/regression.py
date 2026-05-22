from __future__ import annotations

import math
from typing import Sequence


def mae(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    _validate_lengths(y_true, y_pred)
    return sum(abs(float(a) - float(b)) for a, b in zip(y_true, y_pred)) / len(y_true)


def mse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    _validate_lengths(y_true, y_pred)
    return sum((float(a) - float(b)) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)


def rmse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    return math.sqrt(mse(y_true, y_pred))


def r2(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    _validate_lengths(y_true, y_pred)
    mean_true = sum(float(value) for value in y_true) / len(y_true)
    ss_res = sum((float(a) - float(b)) ** 2 for a, b in zip(y_true, y_pred))
    ss_tot = sum((float(a) - mean_true) ** 2 for a in y_true)
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return 1.0 - ss_res / ss_tot


def _validate_lengths(y_true: Sequence[float], y_pred: Sequence[float]) -> None:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if not y_true:
        raise ValueError("Metrics require at least one sample.")
