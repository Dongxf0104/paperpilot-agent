from __future__ import annotations

from paperpilot.baselines.adapters import BaseBaselineAdapter
from paperpilot.baselines.linear_regression_baseline import LinearRegressionBaseline
from paperpilot.baselines.mean_baseline import MeanBaseline


_BASELINES: dict[str, type[BaseBaselineAdapter]] = {
    "mean": MeanBaseline,
    "linear_regression": LinearRegressionBaseline,
}


def register_baseline(name: str, adapter_cls: type[BaseBaselineAdapter]) -> None:
    if not name:
        raise ValueError("Baseline name cannot be empty.")
    _BASELINES[name] = adapter_cls


def create_baseline(name: str, config: dict | None = None) -> BaseBaselineAdapter:
    try:
        cls = _BASELINES[name]
    except KeyError as exc:
        known = ", ".join(sorted(_BASELINES))
        raise KeyError(f"Unknown baseline '{name}'. Known baselines: {known}") from exc
    return cls(config=config)


def list_baselines() -> list[str]:
    return sorted(_BASELINES)
