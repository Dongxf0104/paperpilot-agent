from __future__ import annotations

from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    ("project", "name"),
    ("inputs", "paper"),
    ("inputs", "repository"),
    ("dataset", "path"),
    ("task", "type"),
)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        return [_parse_scalar(part.strip()) for part in body.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _simple_yaml_load(text: str) -> dict[str, Any]:
    """Small YAML subset parser used only when PyYAML is unavailable."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, value = line.strip().partition(":")
        if not key:
            continue
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value.strip():
            parent[key] = _parse_scalar(value)
        else:
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
    return root


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml
    except ImportError:
        return _simple_yaml_load(text)

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Project config must be a mapping: {path}")
    return data


def _get_nested(config: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = config
    for key in path:
        if not isinstance(current, dict) or key not in current:
            dotted = ".".join(path)
            raise ValueError(f"Missing required config field: {dotted}")
        current = current[key]
    return current


def validate_project_config(config: dict[str, Any]) -> None:
    for field in REQUIRED_FIELDS:
        value = _get_nested(config, field)
        if value in (None, ""):
            raise ValueError(f"Required config field cannot be empty: {'.'.join(field)}")

    for list_field in ("metrics", "baselines"):
        value = config.get(list_field)
        if not isinstance(value, list) or not value:
            raise ValueError(f"Config field must be a non-empty list: {list_field}")


def load_project_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(config_path)
    config = _load_yaml(config_path)
    validate_project_config(config)
    config["_config_path"] = str(config_path)
    config["_config_dir"] = str(config_path.parent)
    return config
