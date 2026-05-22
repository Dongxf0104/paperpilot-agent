# Architecture

PaperPilot-Agent is organized around a shared context dictionary. The workflow loads a validated `project.yaml`, then passes context through deterministic agents in a fixed order.

Core layers:

- `paperpilot.core`: config loading, workspace paths, and file I/O.
- `paperpilot.agents`: rule-based planning and reporting agents.
- `paperpilot.baselines`: adapter interface and built-in baselines.
- `paperpilot.metrics`: metric registry and regression metrics.
- `paperpilot.workflow`: orchestration and report writing.

The package intentionally keeps execution lightweight. Richer scanners, runners, and optional LLM integrations can be added behind the existing interfaces without changing the basic workflow.
