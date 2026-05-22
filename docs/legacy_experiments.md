# Legacy Research-Case Experiments

Early exploration around PaperPilot-Agent considered adapters and benchmark cases for DKL, IKL, RF-intRKL, SMOPCA, and related spatial or multi-omics research workflows.

Those experiments are useful as design motivation, but the current open-source version focuses on the generic agent workflow and baseline adapter interface. It does not mix damaged, partial, or project-specific legacy code into the core package.

The intended path is to wrap each third-party research method with a clean `BaseBaselineAdapter` implementation, keep external method code in its own repository or optional integration package, and compare methods through shared datasets, metrics, runner plans, and reports.
