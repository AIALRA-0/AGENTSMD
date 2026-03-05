# STYLE_SUFFIX_MD_2026_03_05_0636

## Metadata

* **Modifier：** Codex
* **Type：** SUFFIX
* **Key：** MD

## Summary

* solidify Markdown Document style rules，Unify title hierarchy、List semantics and code block annotation，Improve readability and maintainability。

## Style Details

* **Format rules：** Title from `#` sequential progression、Leave a blank line between paragraphs、Each line of a list item expresses a complete semantic、Code blocks must have language identifiers。
* **Annotation specifications：** Formal documents are not allowed to be left behind HTML Hide annotations，Temporary notes must be deleted or converted into explicit entries before submission。
* **Naming rules：** Document file names use all uppercase directory prefixes + Semantics Key + Timestamp，Click on the same topic in the directory Key aggregation。
* **Other rules：** Table column names use Chinese business semantics，Avoid mixing Chinese and English column names, which may lead to index misunderstandings。

## Thought

* AGENTSMD The main carrier of the system is Markdown，Inconsistent document styles will directly affect retrieval efficiency and execution accuracy.。
* Title level and code block language annotation are key basic constraints for automatic inspection and fast reading.。
* Reducing annotation noise and naming ambiguity can reduce the complexity of subsequent template verification scripts。

## Action

* press STYLE Template added `Key=MD` suffix style entries and solidify the core rules。
* format、Comment、Name split into independent single line rules，Facilitates script parsing and manual review。
* Synchronous updates `STYLE_INDEX.md`，will `MD` Entries included in searchable index。

## Observation

* This entry can be directly used to constrain all subsequent AGENTSMD Document editing behavior。
* The content of the rules and those currently implemented CHANGEMD/DECISIONMD/ENVIRONMENTMD Write consistently。
* If the rules change in the future，Just update `MD` Same Key entry and refresh the timestamp。
