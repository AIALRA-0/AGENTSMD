# API_TEMPLATE

## Record rules

* APIMD for entry mode（entry），press API Topic `Key` Maintain unified interface specifications。
* same `Key` Keep only one currently valid entry。
* `Key` Update the entry if it already exists and refresh the filename timestamp；`Key` Create a new entry if it does not exist。

## Metadata

* **Modifier：** [actuatorAgentname]
* **Type：** [INTERNAL / EXTERNAL]
* **Key：** [API Subject unique key]

## Summary

* [summary book API The core content of the article，A word is necessary，Single line output]

## Source

* [SRC-001 | Type(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | path orURL | Evidence purposes]
* [SRC-002 | Type(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | path orURL | Evidence purposes]
* [Other source evidence that must be recorded，Multiple outputs possible，One sentence per item]

## Endpoint

* [API-001 | method(GET/POST/PUT/DELETE/...) | path orURL | Function description | Request body/Parameter summary | Successful response summary]
* [API-002 | method(GET/POST/PUT/DELETE/...) | path orURL | Function description | Request body/Parameter summary | Successful response summary]
* [Other interface endpoint details that must be recorded，Multiple outputs possible，One sentence per item]

## Usage

* [Calling scenarios and preconditions，Multiple outputs possible，One sentence per item]
* [Minimum available call example（command orSDK），Multiple outputs possible，One sentence per item]
* [Error handling and retry strategies，Multiple outputs possible，One sentence per item]

## Token Policy

* [Authentication method（Such as Bearer/API-Key/OAuth2），Multiple outputs possible，One sentence per item]
* [token source location（Such as environment variables/Key management system），Multiple outputs possible，One sentence per item]
* [token rotation、Expiration and Permission Boundary Rules，Multiple outputs possible，One sentence per item]
* [Disable writing of real plaintext token，If you need examples use only desensitized placeholders]

## Quota & Maintenance

* [Dosage caliber（Request volume、token、Concurrency、Bandwidth etc.），Multiple outputs possible，One sentence per item]
* [Current limiting/Quota thresholds and over-limit policies，Multiple outputs possible，One sentence per item]
* [Maintenance owner or maintenance process（Upgrade、rollback、Alarm），Multiple outputs possible，One sentence per item]

## Thought

* [This article API Background reasons for the rule，Multiple outputs possible，One sentence per item]
* [Judgment of key constraints and risk boundaries，Multiple outputs possible，One sentence per item]
* [Other interface considerations that must be recorded，Multiple outputs possible，One sentence per item]

## Action

* [The implementation of this entry，Multiple outputs possible，One sentence per item]
* [This linkage update action（Such as SPEC/TEST/TOOL），Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [Access verification and compatibility results，Multiple outputs possible，One sentence per item]
* [for development、test、Maintenance impact，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]
