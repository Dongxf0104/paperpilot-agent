from paperpilot.baselines.registry import create_baseline, list_baselines


def test_registry_creates_builtin_baselines():
    assert "mean" in list_baselines()
    assert "linear_regression" in list_baselines()

    baseline = create_baseline("mean")
    baseline.fit([[0.0], [1.0]], [2.0, 4.0])

    assert baseline.predict([[9.0]]) == [3.0]
