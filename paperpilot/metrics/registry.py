from __future__ import annotations

from collections.abc import Callable, Sequence

from paperpilot.metrics import regression


MetricFn = Callable[[Sequence[float], Sequence[float]], float]

_METRICS: dict[str, MetricFn] = {
    "mae": regression.mae,
    "mse": regression.mse,
    "rmse": regression.rmse,
    "r2": regression.r2,
}


def register_metric(name: str, metric_fn: MetricFn) -> None:
    if not name:
        raise ValueError("Metric name cannot be empty.")
    _METRICS[name.lower()] = metric_fn


def compute_metric(y_true: Sequence[float], y_pred: Sequence[float], metric: str) -> float:
    key = metric.lower()
    try:
        return _METRICS[key](y_true, y_pred)
    except KeyError as exc:
        known = ", ".join(sorted(_METRICS))
        raise KeyError(f"Unknown metric '{metric}'. Known metrics: {known}") from exc


def compute_metrics(y_true: Sequence[float], y_pred: Sequence[float], metrics: Sequence[str]) -> dict[str, float]:
    return {metric: compute_metric(y_true, y_pred, metric) for metric in metrics}
