from __future__ import annotations

import argparse
from pathlib import Path

from paperpilot.workflow.orchestrator import PaperPilotWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="paperpilot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the PaperPilot workflow.")
    run_parser.add_argument("project_config", type=Path, help="Path to project.yaml.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        workflow = PaperPilotWorkflow()
        context = workflow.run(args.project_config)
        report_path = context["outputs"]["report_path"]
        print(f"PaperPilot report written to {report_path}")
        return 0
    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
