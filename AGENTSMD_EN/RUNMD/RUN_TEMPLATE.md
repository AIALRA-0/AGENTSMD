# RUN_TEMPLATE

## Instructions for use

* RUNMD for log mode（log），Record system runtime/Error reporting during operation and maintenance phase、Warning and disposal closed loop。
* This template is only used for running phase events；compile、code、Depend on、Test errors should be written ERRORMD。
* Added each time RUN After recording，Must be updated simultaneously `RUN_INDEX.md`。

## Metadata

* **Modifier：** [actuator Agent Name，For example Codex]
* **event time（UTC）：** [YYYY-MM-DD HH:MM]
* **event name（Key）：** [Stable event name，For example API_HEALTHCHECK_TIMEOUT]
* **Classification：** [DEPLOY / HEALTHCHECK / RESTART / ROLLBACK / INCIDENT / OBSERVABILITY / OTHER]
* **Level：** [FATAL / ERROR / WARNING / NOTICE / INFO / DEBUG]
* **scope of influence：** [service、node、environment or task scope]
* **Status：** [OPEN / RESOLVED / MITIGATED]

## Summary

* [Summarize the core content of this operational event，A word is necessary，Single line output，and should contain“Occurrence time + Number of failures + scope of influence + Recovery results”]

## Thought

* [The basis for judging this running event，Multiple outputs possible，One sentence per item]
* [This risk and impact boundary，Multiple outputs possible，One sentence per item]
* [The goals and priorities of this disposal，Multiple outputs possible，One sentence per item]
* [If there is a time limit target，Clearly state the recovery time limit and recording time limit，Multiple outputs possible，One sentence per item]
* [Other operational thoughts that must be recorded，Multiple outputs possible，One sentence per item]

## Action

* [This troubleshooting step，It is recommended to include precise timestamps（Such as 00:55:30），Multiple outputs possible，One sentence per item]
* [The command or tool used this time，It is recommended to write the original text of key commands，Multiple outputs possible，One sentence per item]
* [This disposal action，It is recommended to write down the action and completion time，Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [Event recurrence results or monitoring alarm content，Recommended number of inclusions、status code、Quantifiable indicators such as response delay，Multiple outputs possible，One sentence per item]
* [Verify results after disposal，It is recommended to include the number of consecutive verifications and key indicators，Multiple outputs possible，One sentence per item]
* [Residual risk or followup observation point，It is recommended to include specific observation periods，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]

## Root Cause

* [The root cause of this incident，Multiple outputs possible，One sentence per item]

## Fix

* [This repair measure，Multiple outputs possible，One sentence per item]

## Prevention

* [Measures to prevent recurrence，Multiple outputs possible，One sentence per item]
