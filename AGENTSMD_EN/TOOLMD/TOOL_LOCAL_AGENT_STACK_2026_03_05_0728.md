# TOOL_LOCAL_AGENT_STACK_2026_03_05_0728

## Metadata

* **Modifier：** Codex
* **Type：** LOCAL
* **Key：** AGENT_STACK

## Summary

* Unified local registration Agent The path to the tool stack、Calling method、Maintain rules and usage boundaries，Support daily development and operation and maintenance execution。

## Tool Details

* TOOL-001 | Codex CLI | LOCAL | /usr/local/bin/codex | codex | terminal main actuator，for code modification、Command execution and process collaboration
* TOOL-002 | Python 3 | LOCAL | /usr/bin/python3 | python3 [script.py] | Run verification script、Data processing scripts and automation tools
* TOOL-003 | Markdown Lint CLI2 | OPEN_SOURCE | /usr/bin/npx | npx markdownlint-cli2 \"**/*.md\" --fix | Markdown Grammar checking and automatic repair
* TOOL-004 | Git | LOCAL | /usr/bin/git | git [command] | Version management and history tracking
* TOOL-005 | Grep | OPEN_SOURCE | /usr/bin/grep | grep \"pattern\" [path] | Quickly retrieve files and locate content

## Usage

* Call precondition：The execution directory should be located at `/aialra/AGENTSMD` or its subdirectories，Avoid cross-project misoperations。
* Minimal call example：`python3 /aialra/AGENTSMD/scripts/md_validate.py --scope TOOLMD` Used to verify tool department entry structure。
* Format checking example：`npx markdownlint-cli2 \"**/*.md\" --fix`，It is necessary to review the automatic repair results after execution.。
* Index synchronization example：`python3 /aialra/AGENTSMD/scripts/md_index_sync.py --scope TOOLMD`，Make sure the index is consistent with the entry。
* Input and output constraints：When the script outputs a failure list, it must be repaired before trying again.，It is forbidden to ignore errors and continue the process.。

## Maintenance

* Maintenance method：Tool paths and versions are regularly inspected by environment maintainers，Entries are updated on demand by the executor。
* Upgrade strategy：Verify compatibility in an isolated environment before upgrading tools，After passing, update the main environment and refresh TOOL entry。
* Rollback strategy：Roll back to the previous stable version when upgrade fails，And in CHANGEMD Record the reasons and results of rollback。
* health check：Perform core tool availability check before each task starts（codex/python3/git/grep/npx）。

## Thought

* Dispersion of tool information leads to repeated trial and error by the executor，Unified registration can significantly reduce path and command inconsistencies.。
* record“path+command+Purpose”ternary information，Can quickly determine whether the tool is missing or the calling method is wrong when troubleshooting。
* Making maintenance strategies explicit reduces the uncertainty introduced by upgrades，Avoid disrupting existing workflows。

## Action

* press TOOL Template reconstruction `AGENT_STACK` Entry and completion tool path、Call examples and maintenance rules。
* Integrate commonly used local execution tools（codex/python3/git/grep/npx）Included in unified tool stack manifest。
* Synchronous updates `TOOL_INDEX.md`，Mark this entry as a currently valid entry。

## Observation

* The current item can be used directly as a tool checklist before executing the task，Reduce disruption caused by environmental differences。
* Tool calling and maintenance rules have been structured and precipitated，Subsequently added tools can be expanded in the same format。
* with AGENTS of entry Consistent specifications，Can be stably parsed by indexing and verification scripts。
