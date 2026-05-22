# PaperPilot-Agent Agent Roles

PaperPilot-Agent uses a fixed sequence of lightweight agents. In the current MVP, these agents are deterministic and rule-based. They are designed to expose the structure of a research benchmark workflow before deeper automation, optional LLM support, or external runners are added.

## Overview

| Agent | Main Responsibility | Adds To Workflow Context |
| --- | --- | --- |
| `PaperReaderAgent` | Reads configured paper metadata. | Paper summary, method keywords, claimed contributions. |
| `CodeScannerAgent` | Inspects the configured local repository path and optional local method repositories. | Entrypoints, dependency hints, repo profiles, adapter plans, risk notes. |
| `BaselineBuilderAgent` | Plans baseline adapter integration. | Baseline adapter plan. |
| `ExperimentDesignerAgent` | Creates the benchmark experiment plan. | Task, dataset, target, metrics, split, seed, baselines. |
| `RunnerPlannerAgent` | Proposes execution steps and outputs. | Commands, runner steps, expected outputs. |
| `ResultAnalystAgent` | Summarizes available benchmark results. | Best method status, metric summary, interpretation. |
| `ConsistencyCheckerAgent` | Checks alignment across the workflow. | Passed checks and warnings. |
| `ReportGeneratorAgent` | Produces the markdown report. | Final report markdown. |

## PaperReaderAgent

**Purpose:** Extract lightweight paper-level signals from the project configuration.

**Input:** `inputs.paper` from `project.yaml`, including optional `path`, `summary`, and `claimed_contributions`.

**Output:** `paper_summary`, `method_keywords`, and `claimed_contributions`.

**Why it matters:** Benchmark workflows often start from a paper claim or method description. Even a short structured summary helps downstream planning stay connected to the original research motivation.

## CodeScannerAgent

**Purpose:** Inspect the configured repository path for dependency and entrypoint hints. When `method_repos` are configured, it also scans those local method repositories and writes human-reviewable repo profiles plus adapter plans.

**Input:** `inputs.repository` and optional `method_repos` from `project.yaml`.

**Output:** `detected_entrypoints`, `detected_dependencies`, `risk_notes`, `repo_profiles`, and `adapter_plan_paths`. Method repo artifacts are written under `outputs/repo_profiles/` and `outputs/adapter_plans/`.

**Why it matters:** Many baseline projects fail at the repository handoff stage. A scanner cannot prove a method is runnable, but it can record README files, dependency files, likely entrypoints, config files, data-loading hints, training files, evaluation files, and missing-path risks for human review.

## BaselineBuilderAgent

**Purpose:** Map each requested baseline to an adapter integration status.

**Input:** `baselines` from `project.yaml`.

**Output:** `baseline_adapter_plan`, including each baseline name, target adapter interface, and whether it is built in or requires an external adapter.

**Why it matters:** Fair benchmark comparison usually requires a common interface. This agent makes explicit whether a baseline can use an existing adapter or still needs integration work.

## ExperimentDesignerAgent

**Purpose:** Build a deterministic benchmark design from the project configuration.

**Input:** `task`, `dataset`, `metrics`, and `baselines` from `project.yaml`.

**Output:** `experiment_plan`, including task type, dataset path, target column, metrics, baseline list, split strategy, and seed.

**Why it matters:** A benchmark is only interpretable when dataset, target, metrics, split, seed, and baselines are aligned. This agent turns scattered configuration fields into one reviewable plan.

## RunnerPlannerAgent

**Purpose:** Create a runnable command suggestion and expected workflow steps.

**Input:** Loaded config path plus the accumulated workflow context.

**Output:** `commands`, `execution_steps`, and `expected_outputs`.

**Why it matters:** Research workflows need a bridge from planning to execution. The current MVP does not run external repositories, but it records the intended local PaperPilot command and the expected report output.

## ResultAnalystAgent

**Purpose:** Summarize result rows when they are provided, or mark analysis as pending.

**Input:** Optional `results` from `project.yaml`, plus configured metrics and baselines.

**Output:** `best_method`, `metric_summary`, and `interpretation`.

**Why it matters:** Benchmark reports should distinguish between completed results and planned experiments. This agent avoids pretending that missing results are real measurements.

## ConsistencyCheckerAgent

**Purpose:** Check whether major workflow components are aligned.

**Input:** Task type, metrics, experiment plan, baseline adapter plan, runner commands, and claimed contributions.

**Output:** `passed_checks` and `warnings`.

**Why it matters:** Consistency checks catch early planning mismatches, such as task-metric mismatch or missing runner steps. In the MVP these checks are intentionally simple, but they provide a place for stronger validation later.

## ReportGeneratorAgent

**Purpose:** Convert the final workflow context into a markdown report.

**Input:** Full accumulated context from all prior agents.

**Output:** `report_markdown`, later written to `outputs/report.md` by the workflow orchestrator.

**Why it matters:** Benchmark work is easier to review when the plan, assumptions, pending results, and consistency checks are captured in one artifact that can be committed, shared, or revised.
