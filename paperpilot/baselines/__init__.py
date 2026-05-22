"""Baseline adapter interface and built-in baselines."""

from paperpilot.baselines.adapters import BaseBaselineAdapter
from paperpilot.baselines.linear_regression_baseline import LinearRegressionBaseline
from paperpilot.baselines.mean_baseline import MeanBaseline
from paperpilot.baselines.registry import create_baseline, list_baselines, register_baseline

__all__ = [
    "BaseBaselineAdapter",
    "MeanBaseline",
    "LinearRegressionBaseline",
    "create_baseline",
    "list_baselines",
    "register_baseline",
]
