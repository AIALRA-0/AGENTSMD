# API_INTERNAL_AUTH_LOGIN_2026_03_05_0712

## Metadata

* **Modifier：** Codex
* **Type：** INTERNAL
* **Key：** AUTH_LOGIN

## Summary

* Solidify internal login authentication API endpoint、Calling method、Authentication policy、Current limiting thresholds and maintenance responsibilities，As a security and regression testing baseline。

## Source

* SRC-001 | Type(LOCAL_FILE) | /aialra/AGENTSMD/SPECMD/SPEC_V1.0.0_2026_03_05_0619.md | Login process and source of specification constraints
* SRC-002 | Type(LOCAL_FILE) | /aialra/AGENTSMD/SECURITYMD/SECURITY_ERROR_LOGIN_BRUTEFORCE_2026_03_05_0055.md | Security risk control and brute force cracking processing constraint sources
* SRC-003 | Type(LOCAL_FILE) | /aialra/AGENTSMD/TESTMD/TEST_STANDARD_QA_BASELINE_2026_03_05_0655.md | Login interface test access control and pass standard sources

## Endpoint

* API-001 | method(POST) | /api/v1/auth/login | User logs in and gets session token | body={email,password,captcha?} | 200 Return access_token/refresh_token summary with user
* API-002 | method(POST) | /api/v1/auth/refresh | Refresh access token | body={refresh_token} | 200 return new access_token
* API-003 | method(POST) | /api/v1/auth/logout | Log out of the current session and undo token | header=Authorization + body={refresh_token?} | 200 Return logout success status

## Usage

* Call precondition：Client must complete captcha or equivalent risk control verification，And the request body field is complete。
* Minimal call example：`curl -X POST https://<host>/api/v1/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"***\",\"password\":\"***\"}'`。
* Error handling：401/403 Do not retry；429 press `Retry-After` Back off and retry；5xx Exponential backoff is used most 3 times。

## Token Policy

* Authentication method：Log in to use `Authorization: Bearer <access_token>` Access protected resources。
* token Source：Server-side issuance JWT，The client only stores short-term access_token，refresh_token receive HttpOnly/Secure cookie protect。
* token life cycle：access_token=15 minutes，refresh_token=7 day；Must log in again after timeout。
* token security boundary：It is forbidden to token write log、Documentation or code repository；Example only allows desensitized placeholders。

## Quota & Maintenance

* Dosage caliber：By number of login requests（QPS）、Failure rate、429 Proportion、Authentication delay（P95）Monitor。
* Current limiting strategy：Single IP Login interface upper limit 60 req/min，Continuous failures exceeding the threshold trigger verification codes and temporary bans。
* Maintenance process：Interface changes require linked updates `SPECMD` with `TESTMD`，After going online, the API Responsible person executes 24h observe。

## Thought

* The login interface carries both the business entrance and the security boundary.，Functional constraints and risk control constraints must be maintained in the same entry.。
* will token Strategies are written as rules rather than explicit text，Balancing enforceability and security compliance。
* Clarifying current limiting and maintenance responsibilities can reduce unclear responsibilities and response delays in the event of online failures.。

## Action

* press APIMD Template reconstruction `AUTH_LOGIN` Entries and completion endpoints、Authentication、Dosage、Maintenance information。
* Unify internal API Example of calling、Error handling and token Management caliber，Lower much Agent access bias。
* Synchronous updates `API_INDEX.md`，Mark this entry as a currently valid entry。

## Observation

* The current entry can directly guide the access to the login interface.、Troubleshooting、Security review and regression testing。
* token The current limiting strategy has been structured and precipitated，Subsequent changes can be made at the same time `Key` Continuous iteration。
* with `SECURITYMD`、`TESTMD`、`SPECMD` The linkage relationship has been clarified，Can support cross-department fast tracking。
