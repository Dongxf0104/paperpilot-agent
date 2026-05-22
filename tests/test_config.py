from paperpilot.core.config import load_project_config


def test_config_loads_example_project():
    config = load_project_config("examples/toy_regression/project.yaml")

    assert config["project"]["name"] == "toy_regression"
    assert config["task"]["type"] == "regression"
    assert "mae" in config["metrics"]
    assert config["baselines"][0]["name"] == "mean"
