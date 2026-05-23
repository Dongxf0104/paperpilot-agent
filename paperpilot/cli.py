from __future__ import annotations

import argparse
from pathlib import Path

from paperpilot.workflows.baseline_planning import BaselinePlanningWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="paperpilot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the baseline-planning agent workflow.")
    run_parser.add_argument("case_config", type=Path, help="Path to case_config.yaml.")

    init_parser = subparsers.add_parser("init-case", help="Create a baseline-planning case template.")
    init_parser.add_argument("case_name", help="Case name to create under cases/.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        context = BaselinePlanningWorkflow().run(args.case_config)
        report_path = context["report_path"]
        print(f"PaperPilot report written to {report_path}")
        return 0
    if args.command == "init-case":
        path = BaselinePlanningWorkflow().init_case(args.case_name)
        print(f"PaperPilot case config written to {path}")
        return 0
    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
