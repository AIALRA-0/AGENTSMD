# SECURITY_TEMPLATE

## Instructions for use

* SECURITYMD for log mode（log），Log only“An attack has occurred or malicious behavior has been confirmed”security incidents。
* This template is used for vulnerability response and security disposal closed loop；Daily safety advice is not written SECURITYMD。
* Added each time SECURITY After recording，Must be updated simultaneously `SECURITY_INDEX.md`。
* Added each time SECURITY while recording，must pass `Linkage` Clear linkage `ERRORMD` or `RUNMD`（at least one）。

## Metadata

* **Modifier：** [actuator Agent Name，For example Codex]
* **event name（Key）：** [Stable event name，For example LOGIN_BRUTEFORCE]
* **Classification：** [ATTACK / INTRUSION / BRUTEFORCE / ABUSE / INCIDENT / OTHER]
* **level：** [FATAL / ERROR / WARNING / NOTICE / INFO / DEBUG]
* **scope of influence：** [service、interface、node、Tenant or data scope]
* **Status：** [OPEN / RESOLVED / MITIGATED]

## Summary

* [Summarize the core content of this security incident，A word is necessary，Single line output，Recommended to include“Attack type + scope of influence + Disposal results”]

## Thought

* [The basis for judging this incident，Multiple outputs possible，One sentence per item]
* [This risk boundary and potential diffusion surface，Multiple outputs possible，One sentence per item]
* [Objectives and technical completion standards for this disposal，Multiple outputs possible，One sentence per item]
* [Other security considerations that must be documented，Multiple outputs possible，One sentence per item]

## Action

* [This disposal step，Just record technical actions，Multiple outputs possible，One sentence per item]
* [The command used this time、strategy or tool，Multiple outputs possible，One sentence per item]
* [This ban、quarantine、Current limiting、Repair action，Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [Alarm、Log、Flow and other observation results，It is recommended to include quantifiable indicators，Multiple outputs possible，One sentence per item]
* [Verify results after disposal，It is recommended to include the number of consecutive verifications and status，Multiple outputs possible，One sentence per item]
* [Residual risk and continuous observation window，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]

## Root Cause

* [The root cause of this security incident，Multiple outputs possible，One sentence per item]

## Fix

* [This repair measure，Multiple outputs possible，One sentence per item]

## Prevention

* [Measures to prevent recurrence，Multiple outputs possible，One sentence per item]

## Linkage

* [LINK-001 | Type(RUN/ERROR) | associated file name | Linkage use]
* [LINK-002 | Type(RUN/ERROR) | associated file name | Linkage use]
* [Other linkage information that must be recorded，Multiple outputs possible，One sentence per item]
