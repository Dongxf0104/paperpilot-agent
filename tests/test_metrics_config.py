from pathlib import Path

from paperpilot.workflows.baseline_planning import _normalize_metrics_config


def test_normalize_metrics_config_accepts_inline_metric_names():
    normalized = _normalize_metrics_config({"metrics": ["mae", "rmse"]})

    assert normalized["metrics_path"] == ""
    assert normalized["metrics_config"] == {"metrics": ["mae", "rmse"]}
    assert normalized["metric_names"] == ["mae", "rmse"]
    assert normalized["warnings"] == []


def test_normalize_metrics_config_accepts_metrics_path(tmp_path: Path):
    metrics_path = tmp_path / "metrics.yaml"
    metrics_path.write_text(
        "metrics:\n"
        "  - name: Accuracy\n"
        "    direction: higher_is_better\n",
        encoding="utf-8",
    )

    normalized = _normalize_metrics_config(
        {"metrics": {"path": "metrics.yaml"}},
        repo_root=tmp_path,
    )

    assert normalized["metrics_path"] == str(metrics_path)
    assert normalized["metric_names"] == ["Accuracy"]
    assert normalized["warnings"] == []
