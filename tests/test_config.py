from paperpilot.core.config import load_project_config


def test_config_loads_example_project():
    config = load_project_config("examples/smopca_minimal/project.yaml")

    assert config["project"]["name"] == "smopca_minimal"
    assert config["task"]["type"] == "regression"
    assert "mae" in config["metrics"]
    assert config["baselines"][0]["name"] == "mean"
