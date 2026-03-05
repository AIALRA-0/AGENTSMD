# SECURITY_ERROR_LOGIN_BRUTEFORCE_2026_03_05_0055

## Metadata

* **Modifier：** Codex
* **event name（Key）：** LOGIN_BRUTEFORCE
* **Classification：** BRUTEFORCE
* **Level：** ERROR
* **scope of influence：** service-agentmd-api Login interface and authentication gateway
* **Status：** MITIGATED

## Summary

* The login interface suffered a brute force attempt（peak 420 req/s），Abnormal traffic drops after disposal 81%，Service returns to normal

## Thought

* Brute force attempt has triggered the alarm threshold（Failure rate >30%），Stop losses immediately to avoid exhaustion of authentication service resources
* risk boundary：If you continue to zoom in，It may cause normal user login failure or DoS Cascade
* disposal target：3 Complete ban and traffic restriction within minutes，10 Complete record and index updates within minutes

## Action

* Positioning /login Endpoint failure rate abnormally spikes to 42.7%，Source IP focus on 3 a /24 Network segment
* execution source IP aggregate analysis，Top3 The attack source request frequency reaches 420 req/s
* Issue WAF Rules for instant ban Top10 IP and high frequency /24 Network segment
* Enable login interface form IP Current limiting（60 req/min）And force the upgrade of the twostep verification code
* Playback authentication log，Confirm that normal users are not accidentally injured

## Observation

* Peak login failure rate before disposal 42.7%，After disposal 5 within minutes 2.1%
* Abnormal traffic drop 81%，The normal login success rate is restored to 99.8% baseline
* No current duration 5xx Error，But need to observe daily 02:00~04:00 Whether the peak source appears IP rotation

## Root Cause

* The login interface lacks layered risk control（IP Reputation + behavior score），Leading to violent attempts to briefly penetrate the first layer of protection

## Fix

* Instant ban high risk IP + activation order IP Current limiting + Forced 2step verification code challenge

## Prevention

* Move login failure aggregate alarm threshold forward（continuous 20 Failures trigger automatic ban recommendation）
* Establish login security incident handling manual（Evidence extraction → ban → Current limiting → Friendly injury review），incorporate RUNBOOKSMD
* Introducing device fingerprints + Behavior scoring layered risk control，Target reduces brute force success rate to <5%

## Linkage

* LINK-001 | RUN | RUN_NOTICE_AGENTMD_API_HEALTH_2026_03_05_0055 | Compare running side stability and recovery verification path，Avoid security disposal impacting service availability
