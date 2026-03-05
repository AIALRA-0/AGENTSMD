# TOOL_TEMPLATE

## Record rules

* TOOLMD for entry mode（entry），By tool topic `Key` Maintain local tool inventory。
* same `Key` Keep only one currently valid entry。
* `Key` Update the entry if it already exists and refresh the filename timestamp；`Key` Create a new entry if it does not exist。

## Metadata

* **Modifier：** [actuatorAgentname]
* **Type：** [LOCAL / OPEN_SOURCE / SERVICE / SCRIPT / MCP / OTHER]
* **Key：** [Tool theme unique key]

## Summary

* [Summarize the core content of this tool record，A word is necessary，Single line output]

## Tool Details

* [TOOL-001 | Tool name | Type | local absolute path | Start command | Usage introduction]
* [TOOL-002 | Tool name | Type | local absolute path | Start command | Usage introduction]
* [Other tool details that must be recorded，Multiple outputs possible，One sentence per item]

## Usage

* [Call precondition（environment variables、Permissions、Depend on），Multiple outputs possible，One sentence per item]
* [Minimal call example（Command or script entry），Multiple outputs possible，One sentence per item]
* [Input and output constraints and common usage，Multiple outputs possible，One sentence per item]

## Maintenance

* [Maintenance person or maintenance method，Multiple outputs possible，One sentence per item]
* [Upgrade/Rollback strategy and version management rules，Multiple outputs possible，One sentence per item]
* [Alarm、Inspection and health check methods，Multiple outputs possible，One sentence per item]

## Thought

* [The background reason for this tool hosting or update，Multiple outputs possible，One sentence per item]
* [This tool boundary and risk judgment，Multiple outputs possible，One sentence per item]
* [Thoughts on other tools that must be recorded，Multiple outputs possible，One sentence per item]

## Action

* [This tool registration or modification action，Multiple outputs possible，One sentence per item]
* [This linkage update action（Such as API/TEST/RUN），Multiple outputs possible，One sentence per item]
* [Other implementation details that must be recorded，Multiple outputs possible，One sentence per item]

## Observation

* [Tool availability verification results，Multiple outputs possible，One sentence per item]
* [Impact on development efficiency and stability，Multiple outputs possible，One sentence per item]
* [Other observation details that must be recorded，Multiple outputs possible，One sentence per item]
