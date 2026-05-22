from __future__ import annotations

import argparse


def load_dataset(path: str) -> list[str]:
    with open(path, encoding="utf-8") as handle:
        return handle.readlines()


def train_model(data: list[str]) -> dict[str, int]:
    return {"rows": max(len(data) - 1, 0)}


def evaluate_model(model: dict[str, int]) -> dict[str, float]:
    return {"mae": float(model["rows"])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = load_dataset(args.data)
    model = train_model(data)
    print({"config": args.config, "output": args.output, "metrics": evaluate_model(model)})


if __name__ == "__main__":
    main()
