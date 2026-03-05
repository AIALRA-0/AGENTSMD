# TEST_STANDARD_QA_BASELINE_2026_03_05_0655

## Metadata

* **Modifier：** Codex
* **Type：** STANDARD
* **Key：** QA_BASELINE

## Summary

* Solidify projectlevel testing and evaluation baselines，Clarify the scope of testing at each stage、Standard threshold、Toolchains and Special Access Requirements。

## Test Matrix

* TEST-001 | AGENTS Rules document changes | REGRESSION | All protected templates are consistent with indexed fields 100% | scripts/md_validate.py | Verify that there are no errors and the index can locate the latest entry
* TEST-002 | Add or update department entries | EVAL | Record structural integrity rate=100%，Required fields must not be missing | scripts/md_validate.py + manual review | Metadata/Summary/The core blocks are complete and the singleline constraints pass
* TEST-003 | Automated script modification | INTEGRATION | lint + validate + index sync All links passed | scripts/check_markdown.sh + scripts/md_sync.sh | All three steps were executed successfully and there was no failure list
* TEST-004 | Prerelease quality gate control | E2E | key workflow（needs analysis/coding implementation/Operational troubleshooting）Can be executed in closed loop by index | manual drill + Script verification | All three workflows can be accessed from AGENTS Jump to the correct department and complete the inventory placement
* TEST-005 | Security incident handling specifications | SECURITY | SECURITY entry Linkage Coverage=100% | scripts/md_validate.py + manual review | each SECURITY Link at least one RUN or ERROR entry

## Special Requirements

* Involves protected files（AGENTS、TEMPLATE、INDEX、Verification script）When changing，External validation must be completed before testing can be performed。
* Exercises involving production environment risks（such as safe disposal、Rollback process）Must use desensitized data and isolation environment，No direct connection to real production credentials。
* Failure of key access control is not allowed“Continue while sick”，Must be repaired before reexecuting the full test loop。

## Thought

* The current framework has entered the multidepartment parallel iteration stage，Without unified testing standards format drift and access control failure will quickly occur。
* Test specifications must cover“Document rule correctness + Automation script executability + Workflow replayability”Three levels of goals。
* Writing standard thresholds into a matrix reduces verbal conventions，Avoid pairs of different executors“Pass”Inconsistent definitions。

## Action

* Create `QA_BASELINE` Subject test items and write into the quantifiable test matrix。
* Script toolchain（lint/validate/sync）Incorporate unified conditions for passing，form a fixed closed loop。
* Synchronous updates `TEST_INDEX.md`，Mark this entry as the currently valid test baseline entry。

## Observation

* Current test items can directly guide subsequent department expansion，No need to redefine test caliber every time。
* Critical quality gates can now be explicitly audited，lower“The rules are written but no one enforces them”risk。
* If new departments or scripts are added later，Just be in the same `Key=QA_BASELINE` The entries are updated iteratively and the timestamp is refreshed。
