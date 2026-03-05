# AGENTSMD global contract

## global principles

* AGENTS before performing any task，This file must be read first。
* Goals of this system：Searchable、traceable、Verifiable、replayable。
* `MD_SYNTAX_CHECK.md` Is the only source of machine rules for structures and fields。
* Protected files start with `REGISTRYMD` The latest entry shall prevail。
* Every task must explicitly select one `workflow_id` and state the reason。
* Every task must add one `RUN_INFO_WORKFLOW_*` trace record，and `Workflow Trace` cannot miss steps。

## Pattern General Principles

### Update correction mode（update）

* Directory：`CHANGEMD`、`DECISIONMD`、`RESEARCHMD`、`REGISTRYMD`、`SPECMD`
* rules：Use this mode in reading logic：Only view the latest version，
* New version，History must be preserved，And the new version should be modified based on the previous historical version；Index only the latest row（The status is `LATEST`）。
* read：By default only the latest version is read；Historical version for tracing。
* Name：`<DEPT>_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`

### log mode（log）

* Directory：`RUNMD`、`ERRORMD`、`SECURITYMD`
* rules：Log by event，Multiple entries of the same type are allowed；Each is an independent event，Does not cover historical events。
* read：Filter required events based on index
* Name：`<DEPT>_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* LEVEL Level：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。

### entry mode（entry）

* Directory：`KNOWLEDGEMD`、`RESOURCEMD`、`ENVIRONMENTMD`、`TOOLMD`、`STYLEMD`、`TESTMD`、`APIMD`
* rules：press `Key` access entry；`Key` Update this if it already exists `Key` current entry，`Key` Create a new entry if it does not exist
* read：Filter required entries based on index
* Common naming：`<DEPT>_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`
* `ENVIRONMENTMD` exception：`<DEPT>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`，Not used TYPE

### Placeholder directory

* Reserve as placeholder directory，Currently not involved in business process reading and writing，but must participate“Strong lock invariance verification”。
* `GOVERNANCEMD`
* `CONTRIBMD`

## General rules for indexing

* AGENT Must read first `*_INDEX.md`，Read the target item again。
* TEMPLATE Define field order；Entries must follow TEMPLATE。
* All schema indexes must contain“Modifier”，Its value comes from the entry `Metadata.Modifier`（For example：`Codex`）。
* Manual tampering with index history lines is prohibited；Indexes are maintained by scripts，Cant help butAGENTmaintenance。
* If the department contains `Source` Field，Must be used uniformly：`SRC-serial number | Type(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | path orURL | Evidence purposes`。

* entry mode（entry）index simplest column（Universal）：`Key | file name | Classification | Modifier | last updated（UTC） | Summary`
* entry mode（entry）Exception index minimal column（ENVIRONMENTMD）：`Key | file name | Modifier | last updated（UTC） | Summary`
* log mode（log）index simplest column：`event time（UTC） | Level | event name | file name | Classification | Modifier | Status | Summary`
* log mode（log）Exception index minimal column（SECURITYMD）：`Level | event name | file name | Classification | Modifier | Status | Summary`
* Update correction mode（update）index simplest column（Universal）：`version number | file name | Modifier | last updated（UTC） | Status | Summary`

## Execution process

1. read `AGENTS.md`。
2. Read target workflow，and select read target department by mode
3. Execute information acquisition according to workflow，Execution and postexecution observations，and update entries as needed
4. If you need to update write，read before write `REGISTRYMD` Latest entry check protection path，If hit protected path，Stop writing and request external confirmation。
5. Must be executed after writing is completed：`scripts/md_sync.sh`。Only used when changing to a separate department：`scripts/md_sync.sh --scope <DEPT>`。
6. If automatic repair fails，Output failure list and alert external users。

## Automated entrance

* Grammar check：`scripts/check_markdown.sh`
* Rule verification：`scripts/md_validate.py [--scope <DEPT>]`
* Index synchronization：`scripts/md_index_sync.py [--scope <DEPT>]`
* Workflow guard：`scripts/md_workflow_guard.py [--scope <DEPT>] [--strict|--report-only]`
* Oneclick closed loop：`scripts/md_sync.sh [--scope <DEPT>]`
* Rule configuration：`MD_SYNTAX_CHECK.md`（If you add a new department or change rules only this file will be modified）

## Workflow template

### Workflow completion rules（force）

* Any workflow that involves writing，Must be executed before writing `REGISTRYMD` protection check（Must be executed even if not explicitly listed）。
* If any workflow produces actual modifications，must contain `CHANGEMD` record。
* Any workflow that involves code、Configuration、Depend on、Interface behavior changes，must contain `TESTMD` Verify。
* If any workflow involves running state impact，must contain `RUNMD` Observation and result writing back。
* Must be executed after any workflow ends“Workflow：Verification and synchronization”。
* Workflow steps are machine-enforced by `MD_SYNTAX_CHECK.md.workflow_enforcement.catalog`。
* Read-only departments must be marked `READ_ONLY` with evidence in `Workflow Trace`; must-write departments must be `CHANGED` with real file diffs。
* Tasks without completed workflow trace cannot be treated as done，and must not skip `md_workflow_guard.py`。

### Workflow：Project initialization（New project access for the first time）

* TOOLMD → ENVIRONMENTMD → REGISTRYMD → SPECMD → RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → STYLEMD → APIMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Rule changes（Add new department/Field/Verification rules）

* AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：Rule conflict fix（Rules inconsistent with actual implementation）

* ERRORMD → AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：needs analysis

* SPECMD → RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → DECISIONMD → CHANGEMD

### Workflow：Resources/knowledge accumulation

* RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → SPECMD → CHANGEMD

### Workflow：coding implementation

* SPECMD → STYLEMD → DECISIONMD → TOOLMD → APIMD → RESOURCEMD → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：API Integrate

* APIMD → TOOLMD → RESOURCEMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：API offline/replace

* APIMD → RESEARCHMD → SPECMD → DECISIONMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Strategy/market correction

* RESEARCHMD → RESOURCEMD → DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：New data resources/replace（Data set、Documentation、patent、Repo）

* RESOURCEMD → KNOWLEDGEMD → RESEARCHMD → SPECMD → CHANGEMD → TESTMD

### Workflow：Specification changes（PRD/Technical specification adjustments）

* RESEARCHMD → SPECMD → DECISIONMD → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：Bug fixes

* ERRORMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD → ENVIRONMENTMD

### Workflow：Operational troubleshooting

* RUNMD → ERRORMD → ENVIRONMENTMD → SECURITYMD → REGISTRYMD → CHANGEMD → TESTMD

### Workflow：security incident

* SECURITYMD → ERRORMD → RUNMD → REGISTRYMD → CHANGEMD → TESTMD → SECURITYMD

### Workflow：Environmental changes（Depend on/system/Operating parameters）

* ENVIRONMENTMD → TOOLMD → SPECMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Tool access and upgrade

* TOOLMD → ENVIRONMENTMD → APIMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Dependency upgrade（language/Library/runtime）

* ENVIRONMENTMD → TOOLMD → SPECMD → APIMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Authentication and permission policy adjustments

* APIMD → SECURITYMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Performance optimization

* RUNMD → ERRORMD → ENVIRONMENTMD → SPECMD → TOOLMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Stability reinforcement（nonattack）

* RUNMD → ERRORMD → ENVIRONMENTMD → REGISTRYMD → SPECMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Update release

* CHANGEMD → TESTMD → SECURITYMD → ENVIRONMENTMD → REGISTRYMD → RUNMD

### Workflow：Final gate before release

* SPECMD → CHANGEMD → TESTMD → SECURITYMD → REGISTRYMD → RUNMD

### Workflow：Postrelease monitoring and corrections

* RUNMD → ERRORMD → SECURITYMD → RESEARCHMD → DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### Workflow：Emergency rollback processing

* RUNMD → SECURITYMD → REGISTRYMD → CHANGEMD → SPECMD → TESTMD → RUNMD

### Workflow：Postevent review and knowledge accumulation

* RUNMD → ERRORMD → SECURITYMD → KNOWLEDGEMD → RESEARCHMD → DECISIONMD → SPECMD → CHANGEMD

### Workflow：Protection policy updates（Protected path changes）

* REGISTRYMD → DECISIONMD → SPECMD → CHANGEMD → TESTMD

### Workflow：Document rules correction（Rules are inconsistent with templates）

* AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → ERRORMD → CHANGEMD → TESTMD

### Workflow：Crossdepartment overhaul（Multiple directory reconstruction）

* DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD → KNOWLEDGEMD

### Workflow：Minimum guarantee process（Unknown scenes，force）

* RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → SPECMD → DECISIONMD → APIMD → TOOLMD → STYLEMD → ENVIRONMENTMD → REGISTRYMD → CHANGEMD → TESTMD → ERRORMD → SECURITYMD → RUNMD
  
### Workflow：Verification and synchronization（Must be placed last）

* After all workflows have run，You all need this script`md_sync.sh`Putting the finishing touches，It contains the following scripts，for reference
* syntax checking script：`bash scripts/check_markdown.sh`
* Rules and Protection Check Script：`python3 scripts/md_validate.py`
* Index update script：`python3 scripts/md_index_sync.py`
* Secondary verification script：`python3 scripts/md_validate.py`
* Oneclick entrance：`bash scripts/md_sync.sh`
  
## APIMD

### Core description

* `APIMD` Used to unify internal and external records API Instructions for use、endpoint definition、Calling method、Authentication token rules、Usage and maintenance information。
* entry mode（entry）。
* The goal is to make Agent In access、Transformation、Troubleshooting API time，Searchable、traceable、Maintainable single point of fact。

### Naming rules

* Use item naming：`API_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Recommended value：`INTERNAL`、`EXTERNAL`。
* `KEY` for API Subject unique key（For example：`AUTH_LOGIN`、`OPENAI_RESPONSES`）。

### Read instructions

* Interface design、Integrate、joint debugging、Before troubleshooting，must be read first `API_INDEX.md` and locate the target `Key`。
* The same task involves multiple API time，The corresponding entries must be read separately，It is forbidden to call based on historical memory。
* Involves authentication、Current limiting、When billing is compatible with version，Read entries first token、Usage and maintenance information。

### Write instructions

* API New、change、When going offline or adjusting strategies，Must be added or updated APIMD entry。
* same `Key` When updating，update this `Key` entries and refresh filename timestamps；`Key` Create a new entry if it does not exist。
* Entry must contain：`Metadata`、`Summary`、`Source`、`Endpoint`、`Usage`、`Token Policy`、`Quota & Maintenance`、`Thought`、`Action`、`Observation`。
* `Source` Must conform to a unified format：`SRC-serial number | Type(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | path orURL | Evidence purposes`。
* `Token Policy` record only token Management rules and source locations，Disable writing of real plaintext token。
* `Quota & Maintenance` Dosage diameter must be recorded、Current limiting/Quota、Maintenance owner or maintenance process。
* Must be updated after writing `API_INDEX.md`，and execute `scripts/md_sync.sh --scope APIMD`。
* API Changes should be linked `SPECMD`、`TESTMD`、`TOOLMD`。

### Prohibited behavior

* Unsourced definitions prohibited API constraint。
* Disable writing of real plaintext token、key or password。
* Disable interface changes and not update APIMD。
* prohibit the same `Key` Keep multiple valid entries in parallel。
  
## CHANGEMD

### Core description

* `CHANGEMD`Used to record each time Modification facts that have been actually implemented and implemented in the system、Causes and consequences，Ensure all changes traceable、Verifiable、Can be rolled back
* Update correction mode（update）
* At least one task at a time CHANGE record；If the task contains multiple independent modification steps，Can generate multiple CHANGE
* Only record system changes that actually occur（code、Configuration、rules、structure、Dependence etc），Do not log pure analysis or reading activities
* `CHANGEMD` Record the change logic and execution process，`Git` Responsible for recording file differences，Both ensure that system changes can be traced
  
### Naming rules

* Use version number to name：`CHANGE_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### Read instructions

* Before executing the task，Read first `CHANGE_INDEX.md` Latest entries，Confirm the current status of the system
* If the task involves a specific module，Need to be in `CHANGE_INDEX.md` Locate the module in the most recent `CHANGE`，and read the corresponding records
* Before regression testing，Read recent changes related to the current module，Confirm that this modification will not break existing behavior
* If found CHANGE Inconsistent with current system status，Priority should be given to the latest CHANGE Check for reference

### Write instructions

* code、Configuration、rules、When the structure or dependencies are actually modified，Must add CHANGE version
* When adding a new entry，Copy`CHANGE_TEMPLATE.md`template，and complete all fields
* New CHANGE The index generation script must be run at the same time`scripts/md_index_sync.py`，Ensure that the index points to the latest record
* Entry must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`。

### Prohibited behavior

* Modification of history is prohibited CHANGE File overwrite fact。
* Disable deletion of history CHANGE record。
* It is forbidden to modify but not write CHANGE。
* It is forbidden to write records that are inconsistent with the actual system modifications。
* If CHANGE Log errors，A correction must be added CHANGE，Instead of modifying the original record。

## DECISIONMD

### Core description

* `DECISIONMD` Used to document architecturelevel decisions（Architecture Decision Records, ADR），Including major technical routes、structural design、Specification changes、Core tradeoffs etc
* Update correction mode（update）
* Only when major version changes occur、Architecture refactoring、Major technology selection、Triggered when core constraints are adjusted
* A major decision corresponds to one DECISION record；If the decision involves multiple independent modules，Can be split into multiple，But each item must be independent and complete
* Only decisions that have reached consensus and entered execution are recorded，No records just discussion、Alternatives or pending issues
* each DECISION After landing，must be in `CHANGEMD` Generate at least one correspondence in CHANGE record

### Naming rules

* Use version number to name：`DECISION_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`
* `MINOR.PATCH` forced to `0.0`，Because only large decisions are recorded

### Read instructions

* Carry out any scheme design、Architectural adjustment、Before technology selection，must be read first `DECISION_INDEX.md` Latest entries in
* If the task involves a specific module or technical direction，first `DECISION_INDEX.md` Locate the most recent time in this direction DECISION，And read the corresponding record in full
* Before regression testing or major changes，Need to trace back the relevant historical decisionmaking chain，Confirm that this action does not violate existing architectural constraints
* If it is found that the current system status is the same as the latest DECISION inconsistent，Priority should be given to the latest DECISION Check for accuracy，and trigger a new decision revision process

### Write instructions

* After an architecturelevel decision occurs and consensus is reached，Must add DECISION version
* When adding a new entry，Copy `DECISION_TEMPLATE.md` template，and complete all fields
* New DECISION The index generation script must be run at the same time `scripts/md_index_sync.py`，Ensure that the index points to the latest record
* Entry must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`
* Once any decision is made，Its execution process must be in `CHANGEMD` Medium leaving traces，at least one CHANGE The record corresponds to this time DECISION

### Prohibited behavior

* It is forbidden to develop ordinary functions、Bug Repair、style adjustment、Configuration change writing DECISION
* Modification or overwriting of history is prohibited DECISION File，To maintain the historical authenticity of decisionmaking
* Disable deletion of history DECISION record
* It is forbidden to make major architectural changes but not write them DECISION
* It is prohibited to write decisionmaking content that is inconsistent with the actual consensus or implementation
* If it is found that there is already DECISION Be biased or out of date，A correction must be added DECISION，Instead of modifying the original record
* prohibited from DECISION Record execution details in

## ENVIRONMENTMD

### Core description

* `ENVIRONMENTMD` Used to record operating environment facts，including operating system、Hardware specifications、Language version、dependency state、Key information such as containers and networks。
* entry mode（entry）。
* same `Key` Keep only one currently valid entry，Read this by default `Key` Latest entries。
* `ENVIRONMENTMD` Not used `TYPE` Classification，Avoid repeated layering of environmental themes。

### Naming rules

* Use versioned entry naming：`ENVIRONMENT_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `KEY` Topics with content for each specific environment

### Read instructions

* Troubleshooting、publish、Before regression testing，read first `ENVIRONMENT_INDEX.md` and locate the target `Key` latest entry。
* If the task involves environmentally sensitive behavior（Depends on installation、System commands、Resource occupation），You must first confirm that the environment entries are consistent with the current machine。
* If it is found that the environmental facts are inconsistent with the latest record in the index，This should be updated first `Key` Current entry and refresh filename timestamp，Continue to perform subsequent tasks。

### Write instructions

* When the environment is first confirmed：Create this new `Key` entry。
* When the environment changes and the `Key` When already exists：update this `Key` entry and update the filename to the latest timestamp。
* Entry must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`。
* `Summary` Must be single line，clear“environment change point + scope of influence”。
* Must be updated synchronously after writing `ENVIRONMENT_INDEX.md`，and execute `scripts/md_sync.sh --scope ENVIRONMENTMD`。

### Prohibited behavior

* prohibit the same `Key` Multiple parallel valid files exist。
* It is forbidden to directly add environment files without skipping the index。
* Disable writing to the running event log ENVIRONMENTMD（Write operational issues RUNMD，engineering error write ERRORMD）。
* Prohibit recording of unverifiable environmental guessing information。

## ERRORMD

### Core description

* `ERRORMD` Record system updates and compilation phases（Nonoperation and maintenance）error、Warning and repair closed loop。
* log mode（log）。
* Each record corresponds to an independent engineering event，Add by event time，Do not overwrite history。
* with `RUNMD` distinguish：`RUNMD` Logging runtime/Operation and maintenance events，`ERRORMD` Record build、compile、code、Depend on、test、Update process events。

### Naming rules

* Unified naming：`ERROR_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` Level：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` Must be a stable event name

### Read instructions

* Read before fixing `ERROR_INDEX.md`，Locate recent records of similar events。
* When the same module fails repeatedly，At least look back at that `Key` of recent 3 history records。
* Read first `FATAL/ERROR` level events，reprocess `WARNING/NOTICE/INFO/DEBUG` Level。

### Write instructions

* Build failed、Compilation failed、Update failed、test failed、dependency conflict、Critical warnings must be written `ERRORMD`。
* The error log must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`。
* `Metadata` must be clearly written `Level`，And with the file name `<LEVEL>` Be consistent。
* If code or configuration modifications are made，Must be linked `CHANGEMD`。
* Must be updated after adding new records `ERROR_INDEX.md`，and execute `scripts/md_sync.sh --scope ERRORMD`。

### Prohibited behavior

* disable runtime/Operation and maintenance events are written to `ERRORMD`（should be written `RUNMD`）。
* It is forbidden to only record error reports without recording repair results。
* Disable overwriting historical error records。
* New additions are prohibited ERROR entry but not updated `ERROR_INDEX.md`。

## KNOWLEDGEMD

### Core description

* `KNOWLEDGEMD` Structured knowledge used to precipitate surveyed data。
* entry mode（entry）。
* Coverage：core explanation、Technical principles、Key concepts、Paper summary、Methodological statement。
* The goal is to make Agent Quickly retrieve and reuse confirmed knowledge before coding and decisionmaking，Avoid duplication of research and understanding costs。

### Naming rules

* Use common naming：`KNOWLEDGE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Recommended value：`CONCEPT`、`PRINCIPLE`、`PAPER`、`METHODOLOGY`、`PATTERN`、`OTHER`。
* `KEY` Must be a stable topic name（upper case+Underline）

### Read instructions

* Encountering complex concepts、When there are differences in technical principles or plans，Read first `KNOWLEDGE_INDEX.md`。
* press `Key` After locating knowledge items，Read the same type first `TYPE` latest record。
* `KNOWLEDGE_INDEX.md` in“Classification”List is `Type`，Its value must match the entry `Metadata.Type` consistent。
* Prioritize reuse of existing methodology and principle items before coding implementation，Avoid repeated explanations and repeated trials and errors。

### Write instructions

* When any new investigative data yields reusable conclusions，All must be added or updated KNOWLEDGE Entries merged into index。
* Same `Key` When content is updated，update this `Key` Current entry and refresh filename timestamp；only in `Key` Create a new entry if it does not exist。
* New entries must contain：`Metadata`、`Summary`、`Source`、`Key Details`、`Thought`、`Action`、`Observation`。
* `Source` Must be traceable：local absolute path or URL，and must conform to a unified format；Unsourced knowledge entries are prohibited。
* Must be updated synchronously after writing `KNOWLEDGE_INDEX.md`，Make sure the index is searchable。

### Prohibited behavior

* Unsourced conclusions or unverifiable explanations are prohibited。
* Disable running logs、Operation and maintenance disposal、Compilation error and repair content are mixed and written to `KNOWLEDGEMD`。
* Disable updating of knowledge items but not updating `KNOWLEDGE_INDEX.md`。

## REGISTRYMD

### Core description

* `REGISTRYMD` Used to record the key points in the project/Important files and paths whitelist。
* Update correction mode（update）。
* When hitting a protected path，Modifications can only be made after external confirmation。
* When a protected path is missed，Can be modified directly according to normal procedures。

### Naming rules

* Use version number to name：`REGISTRY_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### Read instructions

* Read before each write `REGISTRY_INDEX.md` Latest entries。
* Before modifying any file，Use the latest first REGISTRY Entry determines whether the protected path is hit。

### Write instructions

* Only if protection scope or approval policy changes，New REGISTRY version。
* New entries must contain：`Metadata`、`Summary`、`Protected Paths`、`Approval Rule`、`Thought`、`Action`、`Observation`。
* New REGISTRY Must be updated later `REGISTRY_INDEX.md`，and maintain `LATEST/ARCHIVED` Status switching。

### Prohibited behavior

* No skipping REGISTRY Directly change protected files。
* Disable overwriting history REGISTRY entry。
* Disable incorrect registration of unprotected paths as protected paths，Causes normal processes to be blocked unnecessarily。

## RESEARCHMD

### Core description

* `RESEARCHMD` Used to record competitors、competitive market、General environment and key corrections。
* Update correction mode（update）。
* The goal is to ensure Agent Continuously monitor global data and changes in competitive products，and avoid using outdated conclusions to perform tasks。

### Naming rules

* Use version number to name：`RESEARCH_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### Read instructions

* needs assessment、Solution selection、Before strategy adjustment，read first `RESEARCH_INDEX.md` of `LATEST` entry。
* If the task involves a specific competitive product or market theme，It is necessary to review the recent historical research version of this topic for comparison。
* before important decisions，Must confirm if there are new research fixes，Avoid execution driven by outdated market information。

### Write instructions

* new evidence、Changes in competitive products、Market changes、When revising key conclusions，Must add RESEARCH version。
* Entry must contain：`Metadata`、`Summary`、`Source`、`Key Details`、`Thought`、`Action`、`Observation`。
* `Source` Must be traceable：local absolute path or URL，and must conform to a unified format；`Key Details` must contain“old conclusion/new conclusion/scope of influence/priority/evidence”。
* If the research conclusion affects strategy or execution path，Must be linked `DECISIONMD`、`CHANGEMD` or `SPECMD`。
* Must be updated after adding a new version `RESEARCH_INDEX.md`，and execute `scripts/md_sync.sh --scope RESEARCHMD`。

### Prohibited behavior

* It is forbidden to write conclusions without sources。
* It is forbidden to write only the conclusion without writing the key correction details。
* It is prohibited to replace the new version by overwriting the old version。

## RESOURCEMD

### Core description

* `RESOURCEMD` record PDF、patent、Repo、API、Resource paths such as data sets。
* entry mode（entry）。
* Only record the path，Do not store resource text。
* Path rules：Write the local absolute path to the downloaded resource；Resources not downloaded URL。
* same `Key` Keep only one currently valid entry。

### Naming rules

* Use item naming：`RESOURCE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Value suggestions：`DOCS`、`PATENT`、`REPO`、`API`、`DATASET`、`OTHER`。

### Read instructions

* Read before researching `RESOURCE_INDEX.md` Locate available resources。
* Press when reading resources `Key` Locate the currently valid file，No mixing across entries。

### Write instructions

* Absolute path of local resource record；remote resource records URL。
* Same resources `Key` When already exists，update this `Key` entries and refresh filename timestamps。
* Same resources `Key` When it does not exist，New entry。
* Entry must contain：`Metadata`、`Summary`、`Resource Path`、`Thought`、`Action`、`Observation`。
* Must be updated after writing `RESOURCE_INDEX.md`，and execute `scripts/md_sync.sh --scope RESOURCEMD`。

### Prohibited behavior

* prohibit the same `Key` Multiple concurrent valid entries exist。
* It is forbidden to write relative paths to pretend to be local resource paths。
* prohibited from RESOURCEMD Copy and paste the resource content here。

## RUNMD

### Core description

* `RUNMD` Record system runtime/Error reporting during operation and maintenance process、Warning and disposal closed loop。
* log mode（log）。
* Typical scenario：Exception after deployment、Health check failed、Restart recovery、Rollback processing、online incident。
* `RUNMD` Only log events during runtime，Compilation without logging、code、Depend on、test error（These write `ERRORMD`）。

### Naming rules

* Use log naming：`RUN_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` Level：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` Must be a stable event name
  
### Read instructions

* Read before operation and maintenance `RUN_INDEX.md`，Locate recent records of similar events。
* When the same event occurs repeatedly，At least look back at that `Key` Recently 3 history records，Reuse verified repair paths。
* Process first `FATAL/ERROR` Level，reprocess `WARNING/NOTICE/INFO/DEBUG`。

### Write instructions

* Running records must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`。
* `Metadata` must be clearly written `Level`，And with the file name `<LEVEL>` Be consistent。
* `Summary` Must be a single line and contain：Reason for failure，Number of failures、scope of influence、Recovery results。
* `Action` Time stamps and key commands must be recorded as much as possible，Guaranteed playback and reusability。
* `Observation` Must be quantified as much as possible（status code、response delay、Number of consecutive passes、observation period）。
* If running the disposition results in code or configuration changes，Must be linked `CHANGEMD`。
* Must be updated after adding new records `RUN_INDEX.md`，and execute `scripts/md_sync.sh --scope RUNMD`。

### Prohibited behavior

* It is forbidden to write compilation or code errors to RUNMD（should be written `ERRORMD`）。
* New additions are prohibited RUN entries but do not update the index。
* It is prohibited to only record alarms without recording repair results or measures to prevent recurrence。

## SECURITYMD

### Core description

* `SECURITYMD` Used to record the security policy and vulnerability response process after the project is attacked。
* log mode（log）。
* Records must fit Agent Thinking link，At least cover `Thought`、`Action`、`Observation`，Ensure security incidents are traceable、Can be reviewed、Reusable。
* `SECURITYMD` Not ordinary bug Log，Not documenting daytoday advice or preventive discussions that did not occur。

### Naming rules

* `SECURITYMD` Do not use version numbers for naming。
* Use log naming：`SECURITY_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` Level：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` Must be a stable security event name，

### Read instructions

* Before handling security incidents，read first `SECURITY_INDEX.md`，Locate similar historical attack entries。
* combine `ERRORMD` with `RUNMD` associated entries，Reuse authenticated response paths。

### Write instructions

* only in“Under attack or confirmed malicious behavior”Newly added when SECURITY record。
* SECURITY The record must contain：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`、`Linkage`。
* `Summary` Must be a single line and contain：Attack type、scope of influence、Disposal results。
* `Action` Only record technical processing actions and key commands，No timeline required。
* `Observation` Only technical results and verification indicators are recorded，No requirement to record event time。
* `Linkage` Must be associated with at least one `RUNMD` or `ERRORMD` entry，Clarify the file name and linkage purpose。
* After new record is written，Must be appended synchronously to `SECURITY_INDEX.md`。

### Prohibited behavior

* Disable writing when no attack is occurring SECURITY entry。
* prohibited SECURITY Records are not linked `ERRORMD` or `RUNMD`。
* New additions are prohibited SECURITY entry but not updated `SECURITY_INDEX.md`。

## SPECMD

### Core description

* `SPECMD` Used to document the overall project goals、PRD、business goals、User needs、Functional design and technical specification changes。
* Update correction mode（update）。
* The goal is to provide a quick tour of the overall direction and framework of the project，And ensure that the entire specification evolution is traceable。

### Naming rules

* Use version number to name：`SPEC_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### Read instructions

* Requirements clarification、Scheme design、Before development and implementation，read first `SPEC_INDEX.md` of `LATEST` entry。
* If the task involves specification changes，Must review recent history SPEC version，Confirm changing links and boundaries。
* When evaluating implementation options，Must be followed first SPEC Confirmed target、Requirements and technical specifications。

### Write instructions

* overall goal、PRD、business goals、User needs、Functional design、When technical specifications change，Must add SPEC version。
* SPEC The record must contain：`Metadata`、`Summary`、`Spec Details`、`Thought`、`Action`、`Observation`。
* `Spec Details` Must be clearly documented：old specification、New specifications、scope of influence、Priority and acceptance criteria。
* Must be updated after adding a new version `SPEC_INDEX.md`，and maintain `LATEST/ARCHIVED` Status switching。
* Specification changes must be linked `CHANGEMD` with `TESTMD`。

### Prohibited behavior

* Disable overwriting or deletion of history SPEC version。
* It is prohibited to change specifications but not add new ones SPEC version。
* Prohibition of specification changes without linkage CHANGE with TEST。

## STYLEMD

### Core description

* `STYLEMD` Used to define coding and writing style specifications，Include formatting rules、Annotation specifications、Naming rules etc。
* entry mode（entry）。
* to“file suffix”Maintain style entries for your organization，Ensure that different file types have independent and traceable unified rules。

### Naming rules

* Use item naming：`STYLE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Fixed recommended value：`SUFFIX`。
* `KEY` File suffix theme name

### Read instructions

* write code、write documentation、Change comment、Before batch formatting，read first `STYLE_INDEX.md` and locate the target suffix `Key`。
* When the same task involves multiple file suffixes，The corresponding `Key` entry，Do not apply style rules across suffixes。

### Write instructions

* When style rules change，If `Key` If it already exists update it `Key` entries and refresh filename timestamps；If `Key` Create a new entry if it does not exist。
* Entry must contain：`Metadata`、`Summary`、`Style Details`、`Thought`、`Action`、`Observation`。
* `Style Details` Must contain at least：`Format rules`、`Annotation specifications`、`Naming rules`。
* Must be updated synchronously after writing `STYLE_INDEX.md`，and execute `scripts/md_sync.sh --scope STYLEMD`。

### Prohibited behavior

* Prohibited without STYLE Extensively rewrite the format or name according to the following。
* prohibit the same `Key` Keep multiple valid entries in parallel。
* It is forbidden not to update the style rules after they are changed `STYLE_INDEX.md`。

## TESTMD

### Core description

* `TESTMD` Used to define testing and evaluation standards，include“What tests are needed where、what standards to use、what tools to use、What are the special requirements”。
* entry mode（entry）。
* The goal is to make every development、Repair、Releases can all be executed based on unified test specifications，avoid“Changed but didnt test clearly”。

### Naming rules

* Use item naming：`TEST_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Recommended value：`STANDARD`、`ACCEPTANCE`、`EVAL`、`REGRESSION`、`PERFORMANCE`、`SECURITY`、`COMPATIBILITY`、`OTHER`。
* `KEY` Unique key for test subject

### Read instructions

* Requirements review、coding implementation、Must be read before and after publishing `TEST_INDEX.md` and locate the target `Key`。
* When the same task involves multiple modules，Corresponding test items need to be read separately，Not readonly for a single baseline。
* If the standards and tools in the entry cannot overwrite the current changes，Must update first TEST Standardize and execute delivery。

### Write instructions

* Function、interface、Strategy、environment、When dependencies change，Must be added or updated simultaneously TEST entry。
* same `Key` When updating，update this `Key` entries and refresh filename timestamps；`Key` Create a new entry if it does not exist。
* Entry must contain：`Metadata`、`Summary`、`Test Matrix`、`Special Requirements`、`Thought`、`Action`、`Observation`。
* `Test Matrix` Must be clear：Test range、Test type、Test standards、testing tools、pass conditions。
* New additions or updates must be updated simultaneously `TEST_INDEX.md`，and execute `scripts/md_sync.sh --scope TESTMD`。

### Prohibited behavior

* It is forbidden to change requirements without updating test specifications。
* Forbidden to write only“to test”But do not write the standard threshold and passing conditions。
* prohibit the same `Key` Keep multiple valid entries in parallel。

## TOOLMD

### Core description

* `TOOLMD` for listing Agent Available local deployment tools，Include local projects、open source software、Absolute path to the script tool、Introduction、Usage and maintenance information。
* entry mode（entry）。
* The goal is to make Agent Quickly confirm before executing tasks“What tools are available、How to call、what are the boundaries”，Avoid misuse and redundant deployment。

### Naming rules

* Use item naming：`TOOL_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` Recommended value：`LOCAL`、`OPEN_SOURCE`、`SERVICE`、`SCRIPT`、`MCP`、`OTHER`。
* `KEY` Unique key for tool theme（For example：`AGENT_STACK`、`PLAYWRIGHT`、`LANGGRAPH_STUDIO`）。

### Read instructions

* Must be read before executing the task `TOOL_INDEX.md` and locate the target `Key`。
* The local path must be confirmed before calling the tool、Start mode、Input and output constraints and permission boundaries。
* If the index exists but the path is unreachable，Should be updated first TOOL The entry continues to execute。

### Write instructions

* Access to new tools、Path changes、Changes in calling methods、When maintenance information changes，Must be added or updated TOOL entry。
* same `Key` When updating，update this `Key` entries and refresh filename timestamps；`Key` Create a new entry if it does not exist。
* Entry must contain：`Metadata`、`Summary`、`Tool Details`、`Usage`、`Maintenance`、`Thought`、`Action`、`Observation`。
* `Tool Details` Must contain tool type、local absolute path、Start command、Usage introduction。
* Must be updated synchronously after writing `TOOL_INDEX.md`，and execute `scripts/md_sync.sh --scope TOOLMD`。

### Prohibited behavior

* Disable recording of unexecutable pseudocommands or pathless tools。
* It is forbidden to write relative paths to pretend to be local installation paths。
* prohibit the same `Key` Keep multiple valid entries in parallel。
* Prohibit tool from not updating after changes `TOOL_INDEX.md`。

## GOVERNANCEMD

### Core description

* Much Agent Governance placeholder directory，Business process capabilities are currently not implemented。
* The contents of the baseline file must be kept completely unchanged（sha256 strong lock）。

### Naming rules

* Maintain placeholder structure，Not included in business rules。

### Read instructions

* The current main process does not rely on this directory for business decisions by default。

### Write instructions

* Unless the external user explicitly authorizes and updates the lock hash，Otherwise it is prohibited to modify any placeholder files。

### Prohibited behavior

* It is prohibited to use it as a strong dependency in the production process。
* Unauthorized modification of placeholder file contents is prohibited。

## CONTRIBMD

### Core description

* Much Agent Collaboration specification placeholder directory，Business process capabilities are currently not implemented。
* The contents of the baseline file must be kept completely unchanged（sha256 strong lock）。

### Naming rules

* Maintain placeholder structure，Not included in business rules。

### Read instructions

* The current main process does not rely on this directory for business decisions by default。

### Write instructions

* Unless the external user explicitly authorizes and updates the lock hash，Otherwise it is prohibited to modify any placeholder files。

### Prohibited behavior

* It is prohibited to use it as a strong dependency in the production process。
* Unauthorized modification of placeholder file contents is prohibited。

## Protect and enforce the bottom line

* The list of protected files is provided by `REGISTRYMD` Latest version definition。
* Default protected objects include：`AGENTS.md`、`MD_SYNTAX_CHECK.md`、all `*_TEMPLATE.md`、all `*_INDEX.md`、`scripts/md_sync.sh`、`scripts/md_validate.py`、`scripts/md_index_sync.py`、`scripts/check_markdown.sh`。
* No skipping INDEX Write entry directly。
* entry mode（entry）Executed according to departmental rules；`ENVIRONMENTMD` the same `Key` Only one currently valid entry is allowed。
* Disabled in update correction mode（update）Overwrite historical versions。
* disable in log mode（log）Overwrite historical events or mix multiple events into a single record。
* Placeholder words are prohibited in official articles（`TODO`、`TBD`、`[To be added]`）。
* No execution after prohibiting updates `md_sync.sh`。
