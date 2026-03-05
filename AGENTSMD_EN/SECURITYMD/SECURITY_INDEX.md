# SECURITYMD INDEX

## Index description
* This directory is in log mode（log），Add by event，Does not cover historical events。
* Indexes are sorted in descending order of event time，Make it easier to prioritize the latest events。

## Index

| level | event name | file name | Classification | Modifier | Status | Summary |
| --- | --- | --- | --- | --- | --- | --- |
| ERROR | LOGIN_BRUTEFORCE | SECURITY_ERROR_LOGIN_BRUTEFORCE_2026_03_05_0055 | BRUTEFORCE | Codex | MITIGATED | The login interface suffered a brute force attempt（peak 420 req/s），Abnormal traffic drops after disposal 81%，Service returns to normal |
