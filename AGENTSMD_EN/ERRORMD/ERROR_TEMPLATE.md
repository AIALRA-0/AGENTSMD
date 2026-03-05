# ERROR_TEMPLATE

## Instructions for use

* ERRORMD for log mode（log），One record corresponds to one“System update/compile/Engineering process”event。
* This template is only used for nonoperation and maintenance errors and warnings；runtime/Operation and maintenance issues should be written in RUNMD。
* Added each time ERROR After recording，Must be updated simultaneously `ERROR_INDEX.md`。

## Metadata

* **Modifier：** [actuator Agent Name，For example Codex]
* **event time（UTC）：** [YYYY-MM-DD HH:MM]
* **event name（Key）：** [Stable event name，For example BUILD_COMPILE_FAIL]
* **Classification：** [BUILD / COMPILE / UPDATE / DEPENDENCY / TEST / LINT / OTHER]
* **Level：** [FATAL / ERROR / WARNING / NOTICE / INFO / DEBUG]
* **scope of influence：** [module、Directory、Pipeline or build task name]
* **Status：** [OPEN / RESOLVED / MITIGATED]

## Summary

* [Summarize the core content of this error or warning，A word is necessary，Single line output]

## Thought

* [The basis for this error judgment，Multiple outputs possible，One sentence per item]
* [This risk and impact boundary，Multiple outputs possible，One sentence per item]
* [The goals and priorities of this repair，Multiple outputs possible，One sentence per item]
* [Other misconceptions that must be recorded，Multiple outputs possible，One sentence per item]

## Action

* [This troubleshooting step，Multiple outputs possible，One sentence per item]
* [The command or tool used this time，Multiple outputs possible，One sentence per item]
* [This repair action，Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [Error recurrence results or alarm content，Multiple outputs possible，One sentence per item]
* [Verify results after repair，Multiple outputs possible，One sentence per item]
* [Residual risk or followup observation point，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]

## Root Cause

* [The root cause of this error，Multiple outputs possible，One sentence per item]

## Fix

* [This repair measure，Multiple outputs possible，One sentence per item]

## Prevention

* [Measures to prevent recurrence，Multiple outputs possible，One sentence per item]
