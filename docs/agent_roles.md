# Agent Roles

`PaperReaderAgent` reads configured paper metadata and extracts method keywords.

`CodeScannerAgent` inspects a local repository path for dependency and entrypoint hints.

`ExperimentDesignerAgent` turns task, dataset, metric, and baseline settings into an experiment plan.

`BaselineBuilderAgent` maps each baseline to the adapter interface and identifies whether it is built in or external.

`RunnerPlannerAgent` produces reproducible execution steps and command suggestions.

`ResultAnalystAgent` summarizes provided metrics or marks analysis as pending.

`ConsistencyCheckerAgent` checks task, metric, dataset, baseline, and runner-plan alignment.

`ReportGeneratorAgent` turns the context into a markdown report.
