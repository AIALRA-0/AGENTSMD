# RUN_NOTICE_AGENTMD_API_HEALTH_2026_03_05_0055

## Metadata

* **Modifier：** Codex
* **event time（UTC）：** 2026-03-05 00:55
* **event name（Key）：** AGENTMD_API_HEALTH
* **Classification：** HEALTHCHECK
* **Level：** NOTICE
* **scope of influence：** service-agentmd-api
* **Status：** RESOLVED

## Summary

* AGENTMD API Health checks are ongoing 3 failed（probe timeout），Affects all parallel Agent Example，Return to normal after restarting。

## Thought

* Health check failure directly results in Agent Orchestration interruption，Priority must be given to restoring availability rather than immediately digging into the root cause。
* This event is a runtime fluctuation，Not constructed/Compilation error，should be classified as RUNMD rather than ERRORMD。
* risk boundary：If it is caused by restarting dependent services，May cause cascading failure；If it is a memory leak，It is necessary to observe the subsequent peak value。
* Repair target：5 Service restored within minutes，10 Complete event logging and update index within minutes。

## Action

* execute health probe，manual trigger `/healthz` endpoint，Confirm `504 Gateway Timeout`。
* Extract container logs（`kubectl logs agentmd-api-7f8d9c4b5 -n prod --tail=200`），Locate abnormal time window。
* Perform a controlled restart（`kubectl rollout restart deployment/agentmd-api -n prod`）。
* Verify dependency links：Check Redis、PostgreSQL Connection pool status，All normal。
* continuous 5 times probe Pass，Service status returns to green，update `RUN_INDEX.md`。

## Observation

* period probe continuous 3 failed，Return 504，response time greater than 30s。
* After restart probe response time reduced to 180ms，continuous 10 times passed，No recurrence seen。
* There are currently no uservisible errors（API Call log None 5xx），But during peak hours（daily 02:00~04:00）Need to observe stability。
* A single occurrence was found in the log `connection reset by peer`，but did not reappear，Tentatively determined to be instantaneous network jitter。

## Root Cause

* The runtime process exits abnormally for a short period of time（OOM or SIGTERM），Causes the health check probe link to be interrupted。

## Fix

* execute deployment rollout restart，force Pod Rebuild and reestablish the connection pool。

## Prevention

* will `/healthz` probe with Redis/PostgreSQL Selfinspection is added to the postrelease inspection list，Set alarm threshold（continuous 2 failed triggers PagerDuty）。
* Establish a quick handling manual for similar health inspection incidents（5 Restart within minutes + Log extraction + Dependency verification），Deposit RUNBOOKSMD。
* Add container memory monitoring（Prometheus + threshold 85%），in advance 10 minute alarm，avoid OOM resulting in instant exit。
