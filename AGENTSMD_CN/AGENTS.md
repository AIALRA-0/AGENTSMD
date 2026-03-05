# AGENTSMD 全局合同

## 全局原则

* AGENTS 在执行任何任务前，必须先读取本文件。
* 本体系目标：可检索、可追溯、可校验、可回放。
* `MD_SYNTAX_CHECK.md` 是结构与字段的唯一机器规则源。
* 受保护文件以 `REGISTRYMD` 最新条目为准。
* 每次任务必须显式选择一个 `workflow_id` 并说明选择理由。
* 每次任务必须新增一条 `RUN_INFO_WORKFLOW_*` 轨迹记录，且 `Workflow Trace` 不能缺漏步骤。

## 模式总则

### 更新修正模式（update）

* 目录：`CHANGEMD`、`DECISIONMD`、`RESEARCHMD`、`REGISTRYMD`、`SPECMD`
* 规则：在读取逻辑上采用本模式：只看最新版本，
* 新增版本，历史必须保留，且新版本应该基于上一个历史版本修改；索引仅一个最新行（状态为 `LATEST`）。
* 读取：默认只读取最新版本；历史版本用于追溯。
* 命名：`<DEPT>_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`

### 日志模式（log）

* 目录：`RUNMD`、`ERRORMD`、`SECURITYMD`
* 规则：按事件记录，允许同类多条；每条是独立事件，不覆盖历史事件。
* 读取：根据索引筛选所需事件
* 命名：`<DEPT>_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* LEVEL 级别：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。

### 条目模式（entry）

* 目录：`KNOWLEDGEMD`、`RESOURCEMD`、`ENVIRONMENTMD`、`TOOLMD`、`STYLEMD`、`TESTMD`、`APIMD`
* 规则：按 `Key` 访问条目；`Key` 已存在时更新该 `Key` 当前条目，`Key` 不存在时新建条目
* 读取：根据索引筛选所需条目
* 通用命名：`<DEPT>_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`
* `ENVIRONMENTMD` 例外：`<DEPT>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`，不使用 TYPE

### 占位目录

* 保留为占位目录，当前不参与业务流程读写，但必须参与“强锁定不变校验”。
* `GOVERNANCEMD`
* `CONTRIBMD`

## 索引总则

* AGENT 必须先读 `*_INDEX.md`，再读目标条目。
* TEMPLATE 定义字段顺序；条目必须遵循 TEMPLATE。
* 所有模式索引必须包含“修改者”，其值来自条目 `Metadata.修改者`（例如：`Codex`）。
* 禁止手工篡改索引历史行；索引由脚本维护，不由AGENT维护。
* 若部门包含 `Source` 字段，必须统一使用：`SRC-序号 | 类型(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | 路径或URL | 证据用途`。

* 条目模式（entry）索引最简列（通用）：`Key | 文件名 | 分类 | 修改者 | 最后更新（UTC） | 总结`
* 条目模式（entry）例外索引最简列（ENVIRONMENTMD）：`Key | 文件名 | 修改者 | 最后更新（UTC） | 总结`
* 日志模式（log）索引最简列：`事件时间（UTC） | 级别 | 事件名 | 文件名 | 分类 | 修改者 | 状态 | 总结`
* 日志模式（log）例外索引最简列（SECURITYMD）：`级别 | 事件名 | 文件名 | 分类 | 修改者 | 状态 | 总结`
* 更新修正模式（update）索引最简列（通用）：`版本号 | 文件名 | 修改者 | 最后更新（UTC） | 状态 | 总结`

## 执行流程

1. 读取 `AGENTS.md`。
2. 读取目标工作流，并按模式选择读取目标部门
3. 按照工作流执行信息获取，执行和执行后观察，并按需更新条目
4. 如果需要更新写入，写入前读取 `REGISTRYMD` 最新条目检查保护路径，若命中受保护路径，停止写入并请求外部确认。
5. 写入完成后必须执行：`scripts/md_sync.sh`。仅改单独部门时使用：`scripts/md_sync.sh --scope <DEPT>`。
6. 若自动修复失败，输出失败清单并提醒外部用户。

## 自动化入口

* 语法检查：`scripts/check_markdown.sh`
* 规则校验：`scripts/md_validate.py [--scope <DEPT>]`
* 索引同步：`scripts/md_index_sync.py [--scope <DEPT>]`
* 工作流守卫：`scripts/md_workflow_guard.py [--scope <DEPT>] [--strict|--report-only]`
* 一键闭环：`scripts/md_sync.sh [--scope <DEPT>]`
* 规则配置：`MD_SYNTAX_CHECK.md`（新增部门或规则变更只改此文件）

## 工作流模板

### 工作流补全规则（强制）

* 任意工作流若涉及写入，写入前必须执行 `REGISTRYMD` 保护检查（未显式列出也必须执行）。
* 任意工作流若产生实际修改，必须包含 `CHANGEMD` 记录。
* 任意工作流若涉及代码、配置、依赖、接口行为变更，必须包含 `TESTMD` 验证。
* 任意工作流若涉及运行态影响，必须包含 `RUNMD` 观察与结果回写。
* 任意工作流结束后必须执行“工作流：校验与同步”。
* 工作流步骤以 `MD_SYNTAX_CHECK.md.workflow_enforcement.catalog` 为机读准则；文档清单用于理解，不作为脚本唯一判断源。
* 只读部门必须在 `Workflow Trace` 中标记 `READ_ONLY` 并附 evidence；必改部门必须标记 `CHANGED` 且存在真实改动。
* 未完成 workflow trace 的任务不得视为完成，不得跳过 `md_workflow_guard.py`。

### 工作流：项目初始化（新项目第一次接入）

* TOOLMD → ENVIRONMENTMD → REGISTRYMD → SPECMD → RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → STYLEMD → APIMD → CHANGEMD → TESTMD → RUNMD

### 工作流：规则变更（新增部门/字段/校验规则）

* AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：规则冲突修复（规则与实际执行不一致）

* ERRORMD → AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：需求分析

* SPECMD → RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → DECISIONMD → CHANGEMD

### 工作流：资源/知识积累

* RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → SPECMD → CHANGEMD

### 工作流：编码实施

* SPECMD → STYLEMD → DECISIONMD → TOOLMD → APIMD → RESOURCEMD → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：API 集成

* APIMD → TOOLMD → RESOURCEMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：API 下线/替换

* APIMD → RESEARCHMD → SPECMD → DECISIONMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：策略/市场修正

* RESEARCHMD → RESOURCEMD → DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：数据资源新增/替换（数据集、文档、专利、Repo）

* RESOURCEMD → KNOWLEDGEMD → RESEARCHMD → SPECMD → CHANGEMD → TESTMD

### 工作流：规格变更（PRD/技术规格调整）

* RESEARCHMD → SPECMD → DECISIONMD → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：缺陷修复

* ERRORMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD → ENVIRONMENTMD

### 工作流：运行排障

* RUNMD → ERRORMD → ENVIRONMENTMD → SECURITYMD → REGISTRYMD → CHANGEMD → TESTMD

### 工作流：安全事件

* SECURITYMD → ERRORMD → RUNMD → REGISTRYMD → CHANGEMD → TESTMD → SECURITYMD

### 工作流：环境变更（依赖/系统/运行参数）

* ENVIRONMENTMD → TOOLMD → SPECMD → CHANGEMD → TESTMD → RUNMD

### 工作流：工具接入与升级

* TOOLMD → ENVIRONMENTMD → APIMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：依赖升级（语言/库/运行时）

* ENVIRONMENTMD → TOOLMD → SPECMD → APIMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：鉴权与权限策略调整

* APIMD → SECURITYMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：性能优化

* RUNMD → ERRORMD → ENVIRONMENTMD → SPECMD → TOOLMD → CHANGEMD → TESTMD → RUNMD

### 工作流：稳定性加固（非攻击）

* RUNMD → ERRORMD → ENVIRONMENTMD → REGISTRYMD → SPECMD → CHANGEMD → TESTMD → RUNMD

### 工作流：更新发布

* CHANGEMD → TESTMD → SECURITYMD → ENVIRONMENTMD → REGISTRYMD → RUNMD

### 工作流：发布前最终门禁

* SPECMD → CHANGEMD → TESTMD → SECURITYMD → REGISTRYMD → RUNMD

### 工作流：发布后监控与修正

* RUNMD → ERRORMD → SECURITYMD → RESEARCHMD → DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD

### 工作流：紧急回滚处置

* RUNMD → SECURITYMD → REGISTRYMD → CHANGEMD → SPECMD → TESTMD → RUNMD

### 工作流：事后复盘与知识沉淀

* RUNMD → ERRORMD → SECURITYMD → KNOWLEDGEMD → RESEARCHMD → DECISIONMD → SPECMD → CHANGEMD

### 工作流：保护策略更新（受保护路径变更）

* REGISTRYMD → DECISIONMD → SPECMD → CHANGEMD → TESTMD

### 工作流：文档规则纠偏（规则与模板不一致）

* AGENTS.md → MD_SYNTAX_CHECK.md → REGISTRYMD → ERRORMD → CHANGEMD → TESTMD

### 工作流：跨部门大改（多目录重构）

* DECISIONMD → SPECMD → REGISTRYMD → CHANGEMD → TESTMD → RUNMD → KNOWLEDGEMD

### 工作流：保底流程（未知场景兜底，强制）

* RESEARCHMD → RESOURCEMD → KNOWLEDGEMD → SPECMD → DECISIONMD → APIMD → TOOLMD → STYLEMD → ENVIRONMENTMD → REGISTRYMD → CHANGEMD → TESTMD → ERRORMD → SECURITYMD → RUNMD
  
### 工作流：校验与同步（必须放在最后）

* 所有工作流运行后，都需要拿这个脚本`md_sync.sh`进行收尾，其包含如下几个脚本，供参考
* 语法检查脚本：`bash scripts/check_markdown.sh`
* 规则与保护检查脚本：`python3 scripts/md_validate.py`
* 索引更新脚本：`python3 scripts/md_index_sync.py`
* 二次校验脚本：`python3 scripts/md_validate.py`
* 一键入口：`bash scripts/md_sync.sh`
  
## APIMD

### 核心说明

* `APIMD` 用于统一记录内部与外部 API 的使用说明、端点定义、调用方式、鉴权 token 规则、用量与维护信息。
* 条目模式（entry）。
* 目标是让 Agent 在接入、改造、排障 API 时，有可检索、可追溯、可维护的单一事实入口。

### 命名规则

* 使用条目命名：`API_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 建议值：`INTERNAL`、`EXTERNAL`。
* `KEY` 为 API 主题唯一键（例如：`AUTH_LOGIN`、`OPENAI_RESPONSES`）。

### 读取说明

* 接口设计、集成、联调、排障前，必须先读取 `API_INDEX.md` 并定位目标 `Key`。
* 同一任务涉及多个 API 时，必须分别读取对应条目，禁止凭历史记忆调用。
* 涉及鉴权、限流、计费与版本兼容时，优先读取条目中的 token、用量与维护信息。

### 写入说明

* API 新增、变更、下线或策略调整时，必须新增或更新 APIMD 条目。
* 同一 `Key` 更新时，更新该 `Key` 条目并刷新文件名时间戳；`Key` 不存在时新建条目。
* 条目必须包含：`Metadata`、`Summary`、`Source`、`Endpoint`、`Usage`、`Token Policy`、`Quota & Maintenance`、`Thought`、`Action`、`Observation`。
* `Source` 必须符合统一格式：`SRC-序号 | 类型(WEB/PDF/REPORT/REPO/API/LOCAL_FILE/LOG/INTERVIEW/OTHER) | 路径或URL | 证据用途`。
* `Token Policy` 只记录 token 管理规则与来源位置，禁止写入真实明文 token。
* `Quota & Maintenance` 必须记录用量口径、限流/配额、维护责任人或维护流程。
* 写入后必须更新 `API_INDEX.md`，并执行 `scripts/md_sync.sh --scope APIMD`。
* API 变化应联动 `SPECMD`、`TESTMD`、`TOOLMD`。

### 禁止行为

* 禁止无来源定义 API 约束。
* 禁止写入真实明文 token、密钥或密码。
* 禁止接口变化不更新 APIMD。
* 禁止同一 `Key` 保留多个并行有效条目。
  
## CHANGEMD

### 核心说明

* `CHANGEMD`用于记录每次 已实际执行并落地到系统中的修改事实、原因与结果，确保所有变更 可追溯、可验证、可回滚
* 更新修正模式（update）
* 一次任务至少一条 CHANGE 记录；若任务包含多个独立修改步骤，可生成多条 CHANGE
* 仅记录真实发生的系统变更（代码、配置、规则、结构、依赖等），不记录纯分析或阅读行为
* `CHANGEMD` 记录变更逻辑与执行过程，`Git` 负责记录文件差异，两者共同保证系统变更可追踪
  
### 命名规则

* 使用版本号命名：`CHANGE_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### 读取说明

* 实施任务前，先读 `CHANGE_INDEX.md` 最新条目，确认系统当前状态
* 若任务涉及特定模块，需在 `CHANGE_INDEX.md` 中定位该模块最近一次 `CHANGE`，并阅读对应记录
* 回归测试前，读与当前模块相关的最近变更，确认本次修改不会破坏既有行为
* 若发现 CHANGE 与当前系统状态不一致，应优先以最新 CHANGE 为参考进行检查

### 写入说明

* 代码、配置、规则、结构或依赖发生实际修改时，必须新增 CHANGE 版本
* 新增条目时，复制`CHANGE_TEMPLATE.md`的模板，并完成填写所有字段
* 新增 CHANGE 时必须同时运行索引生成脚本`scripts/md_index_sync.py`，保证索引能够指向最新记录
* 条目必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`。

### 禁止行为

* 禁止修改历史 CHANGE 文件覆盖事实。
* 禁止删除历史 CHANGE 记录。
* 禁止有修改但不写 CHANGE。
* 禁止写入与实际系统修改不一致的记录。
* 若 CHANGE 记录错误，必须新增一条修正 CHANGE，而不是修改原记录。

## DECISIONMD

### 核心说明

* `DECISIONMD` 用于记录架构级决策（Architecture Decision Records, ADR），包括重大技术路线、结构设计、规范变更、核心权衡等
* 更新修正模式（update）
* 仅在发生大版本变更、架构重构、重大技术选型、核心约束调整时触发
* 一次重大决策对应一条 DECISION 记录；若决策涉及多个独立模块，可拆分为多条，但每条必须独立完整
* 仅记录已达成共识并进入执行的决策，不记录纯讨论、备选方案或未决事项
* 每条 DECISION 落地后，必须在 `CHANGEMD` 中至少生成一条对应 CHANGE 记录

### 命名规则

* 使用版本号命名：`DECISION_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`
* `MINOR.PATCH` 强制为 `0.0`，因为只记录大型决策

### 读取说明

* 进行任何方案设计、架构调整、技术选型前，必须先读取 `DECISION_INDEX.md` 中的最新条目
* 若任务涉及特定模块或技术方向，先在 `DECISION_INDEX.md` 中定位该方向最近一次 DECISION，并完整阅读对应记录
* 回归测试或重大变更前，需回溯相关历史决策链，确认本次动作不违反既有架构约束
* 若发现当前系统状态与最新 DECISION 不一致，应优先以最新 DECISION 为准进行检查，并触发新的决策修正流程

### 写入说明

* 发生架构级决策并达成共识后，必须新增 DECISION 版本
* 新增条目时，复制 `DECISION_TEMPLATE.md` 的模板，并完整填写所有字段
* 新增 DECISION 时必须同时运行索引生成脚本 `scripts/md_index_sync.py`，保证索引能够指向最新记录
* 条目必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`
* 任何决策一旦落地，其执行过程必须在 `CHANGEMD` 中留痕，至少一条 CHANGE 记录对应本次 DECISION

### 禁止行为

* 禁止将普通功能开发、Bug 修复、风格调整、配置变更写入 DECISION
* 禁止修改或覆盖历史 DECISION 文件，以维护决策历史真实性
* 禁止删除历史 DECISION 记录
* 禁止有重大架构变更但不写 DECISION
* 禁止写入与实际共识或落地不一致的决策内容
* 若发现已有 DECISION 存在偏差或过时，必须新增一条修正 DECISION，而不是修改原记录
* 禁止在 DECISION 中记录执行细节

## ENVIRONMENTMD

### 核心说明

* `ENVIRONMENTMD` 用于记录运行环境事实，包括操作系统、硬件规格、语言版本、依赖状态、容器与网络等关键信息。
* 条目模式（entry）。
* 同一 `Key` 仅保留一个当前有效条目，默认读取该 `Key` 最新条目。
* `ENVIRONMENTMD` 不使用 `TYPE` 分类，避免环境主题被重复分层。

### 命名规则

* 使用版本化条目命名：`ENVIRONMENT_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `KEY` 为每个具体环境内容的主题

### 读取说明

* 排障、发布、回归测试前，先读取 `ENVIRONMENT_INDEX.md` 并定位目标 `Key` 的最新条目。
* 若任务涉及环境敏感行为（依赖安装、系统命令、资源占用），必须先确认环境条目与当前机器一致。
* 若发现环境事实与索引最新记录不一致，应先更新该 `Key` 当前条目并刷新文件名时间戳，再继续执行后续任务。

### 写入说明

* 当环境首次确认时：新建该 `Key` 条目。
* 当环境发生变化且该 `Key` 已存在时：更新该 `Key` 条目并将文件名更新为最新时间戳。
* 条目必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`。
* `Summary` 必须单行，明确“环境变更点 + 影响范围”。
* 写入后必须同步更新 `ENVIRONMENT_INDEX.md`，并执行 `scripts/md_sync.sh --scope ENVIRONMENTMD`。

### 禁止行为

* 禁止同一 `Key` 存在多个并行有效文件。
* 禁止跳过索引直接新增环境文件。
* 禁止把运行事件日志写入 ENVIRONMENTMD（运行问题写 RUNMD，工程错误写 ERRORMD）。
* 禁止记录无法验证的环境猜测信息。

## ERRORMD

### 核心说明

* `ERRORMD` 记录系统更新与编译阶段（非运维）的错误、警告与修复闭环。
* 日志模式（log）。
* 每条记录对应一次独立工程事件，按事件时间新增，不覆盖历史。
* 与 `RUNMD` 区分：`RUNMD` 记录运行时/运维事件，`ERRORMD` 记录构建、编译、代码、依赖、测试、更新流程事件。

### 命名规则

* 统一命名：`ERROR_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` 级别：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` 必须是稳定事件名

### 读取说明

* 修复前先读取 `ERROR_INDEX.md`，定位同类事件最近记录。
* 涉及同模块反复失败时，至少回看该 `Key` 的最近 3 条历史记录。
* 优先读取 `FATAL/ERROR` 级别事件，再处理 `WARNING/NOTICE/INFO/DEBUG` 级别。

### 写入说明

* 构建失败、编译失败、更新失败、测试失败、依赖冲突、关键警告都必须写入 `ERRORMD`。
* 错误记录必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`。
* `Metadata` 必须明确写 `级别`，并与文件名中的 `<LEVEL>` 保持一致。
* 若产生代码或配置修改，必须联动 `CHANGEMD`。
* 新增记录后必须更新 `ERROR_INDEX.md`，并执行 `scripts/md_sync.sh --scope ERRORMD`。

### 禁止行为

* 禁止把运行时/运维事件写到 `ERRORMD`（应写入 `RUNMD`）。
* 禁止只记录报错不记录修复结果。
* 禁止覆盖历史错误记录。
* 禁止新增 ERROR 条目但不更新 `ERROR_INDEX.md`。

## KNOWLEDGEMD

### 核心说明

* `KNOWLEDGEMD` 用于沉淀已调查资料的结构化知识。
* 条目模式（entry）。
* 覆盖范围：核心解释、技术原理、关键概念、论文总结、方法论说明。
* 目标是让 Agent 在编码与决策前可以快速检索并复用已确认知识，避免重复调研与重复理解成本。

### 命名规则

* 使用通用命名：`KNOWLEDGE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 建议值：`CONCEPT`、`PRINCIPLE`、`PAPER`、`METHODOLOGY`、`PATTERN`、`OTHER`。
* `KEY` 必须是稳定主题名（大写+下划线）

### 读取说明

* 遇到复杂概念、技术原理或方案分歧时，先读 `KNOWLEDGE_INDEX.md`。
* 按 `Key` 定位知识条目后，优先读取同类 `TYPE` 的最新记录。
* `KNOWLEDGE_INDEX.md` 中的“分类”列即 `Type`，其值必须与条目 `Metadata.Type` 一致。
* 编码实施前优先复用已有方法论和原理条目，避免重复解释与重复试错。

### 写入说明

* 任何新调查资料产生了可复用结论时，都必须新增或更新 KNOWLEDGE 条目并入索引。
* 同 `Key` 内容更新时，更新该 `Key` 当前条目并刷新文件名时间戳；仅在 `Key` 不存在时新建条目。
* 新条目必须包含：`Metadata`、`Summary`、`Source`、`Key Details`、`Thought`、`Action`、`Observation`。
* `Source` 必须可追溯：本地绝对路径或 URL，且必须符合统一格式；禁止无来源知识条目。
* 写入后必须同步更新 `KNOWLEDGE_INDEX.md`，确保索引可检索。

### 禁止行为

* 禁止无来源结论或不可验证解释。
* 禁止把运行日志、运维处置、编译报错修复内容混写到 `KNOWLEDGEMD`。
* 禁止更新知识条目但不更新 `KNOWLEDGE_INDEX.md`。

## REGISTRYMD

### 核心说明

* `REGISTRYMD` 用于记录项目里的关键/重要文件与路径白名单。
* 更新修正模式（update）。
* 命中受保护路径时，必须外部确认后才能修改。
* 未命中受保护路径时，可按正常流程直接修改。

### 命名规则

* 使用版本号命名：`REGISTRY_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### 读取说明

* 每次写入前先读取 `REGISTRY_INDEX.md` 最新条目。
* 修改任意文件前，先用最新 REGISTRY 条目判断是否命中受保护路径。

### 写入说明

* 仅当保护范围或审批策略变化时，新增 REGISTRY 版本。
* 新条目必须包含：`Metadata`、`Summary`、`Protected Paths`、`Approval Rule`、`Thought`、`Action`、`Observation`。
* 新增 REGISTRY 后必须更新 `REGISTRY_INDEX.md`，并维护 `LATEST/ARCHIVED` 状态切换。

### 禁止行为

* 禁止跳过 REGISTRY 直接改受保护文件。
* 禁止覆盖历史 REGISTRY 条目。
* 禁止把非保护路径错误登记为受保护路径，导致正常流程被不必要阻塞。

## RESEARCHMD

### 核心说明

* `RESEARCHMD` 用于记录竞争对手、竞争市场、大环境与关键修正。
* 更新修正模式（update）。
* 目标是保证 Agent 对全局资料与竞品变化的持续把控，并避免使用过时结论执行任务。

### 命名规则

* 使用版本号命名：`RESEARCH_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### 读取说明

* 需求评估、方案选型、策略调整前，先读取 `RESEARCH_INDEX.md` 的 `LATEST` 条目。
* 若任务涉及特定竞品或市场主题，需回看该主题最近的历史研究版本用于对照。
* 重要决策前，必须确认是否存在新的研究修正，避免以过时市场信息驱动执行。

### 写入说明

* 新证据、竞品变化、市场变化、关键结论修正时，必须新增 RESEARCH 版本。
* 条目必须包含：`Metadata`、`Summary`、`Source`、`Key Details`、`Thought`、`Action`、`Observation`。
* `Source` 必须可追溯：本地绝对路径或 URL，且必须符合统一格式；`Key Details` 必须包含“旧结论/新结论/影响范围/优先级/证据”。
* 若研究结论影响策略或执行路径，必须联动 `DECISIONMD`、`CHANGEMD` 或 `SPECMD`。
* 新增版本后必须更新 `RESEARCH_INDEX.md`，并执行 `scripts/md_sync.sh --scope RESEARCHMD`。

### 禁止行为

* 禁止无来源写结论。
* 禁止只写结论不写关键修正细节。
* 禁止用覆盖旧版本代替新增版本。

## RESOURCEMD

### 核心说明

* `RESOURCEMD` 记录 PDF、专利、Repo、API、数据集等资源路径。
* 条目模式（entry）。
* 仅记录路径，不存放资源正文。
* 路径规则：已下载资源写本地绝对路径；未下载资源写 URL。
* 同一 `Key` 仅保留一个当前有效条目。

### 命名规则

* 使用条目命名：`RESOURCE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 取值建议：`DOCS`、`PATENT`、`REPO`、`API`、`DATASET`、`OTHER`。

### 读取说明

* 调研前先读 `RESOURCE_INDEX.md` 定位可用资源。
* 读取资源时按 `Key` 定位当前有效文件，不跨条目混读。

### 写入说明

* 本地资源记录绝对路径；远程资源记录 URL。
* 同资源 `Key` 已存在时，更新该 `Key` 条目并刷新文件名时间戳。
* 同资源 `Key` 不存在时，新增条目。
* 条目必须包含：`Metadata`、`Summary`、`Resource Path`、`Thought`、`Action`、`Observation`。
* 写入后必须更新 `RESOURCE_INDEX.md`，并执行 `scripts/md_sync.sh --scope RESOURCEMD`。

### 禁止行为

* 禁止同一 `Key` 存在多个并行有效条目。
* 禁止写相对路径冒充本地资源路径。
* 禁止在 RESOURCEMD 里复制粘贴资源正文内容。

## RUNMD

### 核心说明

* `RUNMD` 记录系统运行时/运维过程的报错、警告与处置闭环。
* 日志模式（log）。
* 典型场景：部署后异常、健康检查失败、重启恢复、回滚处置、线上 incident。
* `RUNMD` 只记录运行阶段事件，不记录编译、代码、依赖、测试错误（这些写入 `ERRORMD`）。

### 命名规则

* 使用日志命名：`RUN_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` 级别：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` 必须是稳定事件名
  
### 读取说明

* 运维操作前先读取 `RUN_INDEX.md`，定位同类事件最近记录。
* 同一事件重复发生时，至少回看该 `Key` 最近 3 条历史记录，复用已验证修复路径。
* 先处理 `FATAL/ERROR` 级别，再处理 `WARNING/NOTICE/INFO/DEBUG`。

### 写入说明

* 运行记录必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`。
* `Metadata` 必须明确写 `级别`，并与文件名中的 `<LEVEL>` 保持一致。
* `Summary` 必须单行且包含：失败原因，失败次数、影响范围、恢复结果。
* `Action` 必须尽量记录时间戳与关键命令，保证可回放与可复用。
* `Observation` 必须尽量量化（状态码、响应时延、连续通过次数、观察时段）。
* 若运行处置导致代码或配置改动，必须联动 `CHANGEMD`。
* 新增记录后必须更新 `RUN_INDEX.md`，并执行 `scripts/md_sync.sh --scope RUNMD`。

### 禁止行为

* 禁止把编译或代码错误写到 RUNMD（应写 `ERRORMD`）。
* 禁止新增 RUN 条目但不更新索引。
* 禁止只记录告警不记录修复结果或防再发措施。

## SECURITYMD

### 核心说明

* `SECURITYMD` 用于记录项目遭受攻击后的安全策略与漏洞响应流程。
* 日志模式（log）。
* 记录必须贴合 Agent 思维链路，至少覆盖 `Thought`、`Action`、`Observation`，确保安全事件可追溯、可复盘、可复用。
* `SECURITYMD` 不是普通 bug 日志，不记录未发生攻击的日常建议或预防性讨论。

### 命名规则

* `SECURITYMD` 不使用版本号命名。
* 使用日志命名：`SECURITY_<LEVEL>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `LEVEL` 级别：`FATAL`、`ERROR`、`WARNING`、`NOTICE`、`INFO`、`DEBUG`。
* `KEY` 必须是稳定安全事件名，

### 读取说明

* 安全事件处置前，先读取 `SECURITY_INDEX.md`，定位同类历史攻击条目。
* 结合 `ERRORMD` 与 `RUNMD` 的关联条目，复用已验证的响应路径。

### 写入说明

* 仅在“遭受攻击或确认恶意行为”时新增 SECURITY 记录。
* SECURITY 记录必须包含：`Metadata`、`Summary`、`Thought`、`Action`、`Observation`、`Root Cause`、`Fix`、`Prevention`、`Linkage`。
* `Summary` 必须单行且包含：攻击类型、影响范围、处置结果。
* `Action` 只记录技术处置动作与关键命令，不要求记录时间线。
* `Observation` 只记录技术结果与验证指标，不要求记录事件时间。
* `Linkage` 必须至少关联一个 `RUNMD` 或 `ERRORMD` 条目，明确文件名与联动用途。
* 新记录写入后，必须同步追加到 `SECURITY_INDEX.md`。

### 禁止行为

* 禁止在未发生攻击时写入 SECURITY 条目。
* 禁止 SECURITY 记录不联动 `ERRORMD` 或 `RUNMD`。
* 禁止新增 SECURITY 条目但不更新 `SECURITY_INDEX.md`。

## SPECMD

### 核心说明

* `SPECMD` 用于记录项目总体目标、PRD、商业目标、用户需求、功能设计与技术规格变动。
* 更新修正模式（update）。
* 目标是提供项目总体方向与框架的快速导览，并保证规格演进全程可追溯。

### 命名规则

* 使用版本号命名：`SPEC_V<MAJOR>.<MINOR>.<PATCH>_<YYYY>_<MM>_<DD>_<HHMM>.md`。

### 读取说明

* 需求澄清、方案设计、开发实施前，先读取 `SPEC_INDEX.md` 的 `LATEST` 条目。
* 若任务涉及规格变更，必须回看最近历史 SPEC 版本，确认变更链路与边界。
* 评估实现方案时，必须优先遵循 SPEC 中已确认的目标、需求与技术规格。

### 写入说明

* 总体目标、PRD、商业目标、用户需求、功能设计、技术规格发生变动时，必须新增 SPEC 版本。
* SPEC 记录必须包含：`Metadata`、`Summary`、`Spec Details`、`Thought`、`Action`、`Observation`。
* `Spec Details` 必须明确记录：旧规格、新规格、影响范围、优先级与验收标准。
* 新增版本后必须更新 `SPEC_INDEX.md`，并维护 `LATEST/ARCHIVED` 状态切换。
* 规格变化必须联动 `CHANGEMD` 与 `TESTMD`。

### 禁止行为

* 禁止覆盖或删除历史 SPEC 版本。
* 禁止规格发生变动但不新增 SPEC 版本。
* 禁止规格变更不联动 CHANGE 与 TEST。

## STYLEMD

### 核心说明

* `STYLEMD` 用于定义代码与写作风格规范，包括格式规则、注释规范、命名规则等。
* 条目模式（entry）。
* 以“文件后缀”为单位维护风格条目，确保不同文件类型有独立且可追溯的统一规则。

### 命名规则

* 使用条目命名：`STYLE_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 固定建议值：`SUFFIX`。
* `KEY` 为文件后缀主题名

### 读取说明

* 写代码、写文档、改注释、批量格式化前，先读取 `STYLE_INDEX.md` 并定位目标后缀 `Key`。
* 同一任务涉及多种文件后缀时，必须分别读取对应 `Key` 条目，禁止跨后缀套用风格规则。

### 写入说明

* 风格规则变更时，若 `Key` 已存在则更新该 `Key` 条目并刷新文件名时间戳；若 `Key` 不存在则新建条目。
* 条目必须包含：`Metadata`、`Summary`、`Style Details`、`Thought`、`Action`、`Observation`。
* `Style Details` 必须至少包含：`格式规则`、`注释规范`、`命名规则`。
* 写入后必须同步更新 `STYLE_INDEX.md`，并执行 `scripts/md_sync.sh --scope STYLEMD`。

### 禁止行为

* 禁止在无 STYLE 依据下大范围改写格式或命名。
* 禁止同一 `Key` 保留多个并行有效条目。
* 禁止风格规则变更后不更新 `STYLE_INDEX.md`。

## TESTMD

### 核心说明

* `TESTMD` 用于定义测试与评估标准，包括“什么地方需要什么测试、使用什么标准、使用什么工具、有哪些特殊要求”。
* 条目模式（entry）。
* 目标是让每次开发、修复、发布都能基于统一测试规范执行，避免“改了但没测清楚”。

### 命名规则

* 使用条目命名：`TEST_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 建议值：`STANDARD`、`ACCEPTANCE`、`EVAL`、`REGRESSION`、`PERFORMANCE`、`SECURITY`、`COMPATIBILITY`、`OTHER`。
* `KEY` 为测试主题唯一键

### 读取说明

* 需求评审、编码实施、发布前后都必须先读取 `TEST_INDEX.md` 并定位目标 `Key`。
* 同一任务涉及多个模块时，需分别读取对应测试条目，不可只读单一基线。
* 若条目中的标准与工具无法覆盖当前改动，必须先更新 TEST 规范再执行交付。

### 写入说明

* 功能、接口、策略、环境、依赖发生变化时，必须同步新增或更新 TEST 条目。
* 同一 `Key` 更新时，更新该 `Key` 条目并刷新文件名时间戳；`Key` 不存在时新建条目。
* 条目必须包含：`Metadata`、`Summary`、`Test Matrix`、`Special Requirements`、`Thought`、`Action`、`Observation`。
* `Test Matrix` 必须明确：测试范围、测试类型、测试标准、测试工具、通过条件。
* 新增或更新后必须同步更新 `TEST_INDEX.md`，并执行 `scripts/md_sync.sh --scope TESTMD`。

### 禁止行为

* 禁止有需求变更但无测试规范更新。
* 禁止只写“要测试”但不写标准阈值与通过条件。
* 禁止同一 `Key` 保留多个并行有效条目。

## TOOLMD

### 核心说明

* `TOOLMD` 用于列出 Agent 可用的本地部署工具，包括本地项目、开源软件、脚本工具的绝对路径、简介、用法与维护信息。
* 条目模式（entry）。
* 目标是让 Agent 在执行任务前能快速确认“有哪些工具可用、怎么调用、有什么边界”，避免误用与重复部署。

### 命名规则

* 使用条目命名：`TOOL_<TYPE>_<KEY>_<YYYY>_<MM>_<DD>_<HHMM>.md`。
* `TYPE` 建议值：`LOCAL`、`OPEN_SOURCE`、`SERVICE`、`SCRIPT`、`MCP`、`OTHER`。
* `KEY` 为工具主题唯一键（例如：`AGENT_STACK`、`PLAYWRIGHT`、`LANGGRAPH_STUDIO`）。

### 读取说明

* 执行任务前必须先读取 `TOOL_INDEX.md` 并定位目标 `Key`。
* 调用工具前必须确认本地路径、启动方式、输入输出约束与权限边界。
* 若索引存在但路径不可达，应先更新 TOOL 条目再继续执行。

### 写入说明

* 新工具接入、路径变化、调用方式变化、维护信息变化时，必须新增或更新 TOOL 条目。
* 同一 `Key` 更新时，更新该 `Key` 条目并刷新文件名时间戳；`Key` 不存在时新建条目。
* 条目必须包含：`Metadata`、`Summary`、`Tool Details`、`Usage`、`Maintenance`、`Thought`、`Action`、`Observation`。
* `Tool Details` 必须包含工具类型、本地绝对路径、启动命令、用途简介。
* 写入后必须同步更新 `TOOL_INDEX.md`，并执行 `scripts/md_sync.sh --scope TOOLMD`。

### 禁止行为

* 禁止记录无法执行的伪命令或无路径工具。
* 禁止写相对路径冒充本地安装路径。
* 禁止同一 `Key` 保留多个并行有效条目。
* 禁止工具变更后不更新 `TOOL_INDEX.md`。

## GOVERNANCEMD

### 核心说明

* 多 Agent 治理占位目录，当前暂不实现业务流程能力。
* 必须保持基线文件内容完全不变（sha256 强锁定）。

### 命名规则

* 维持占位结构，不纳入业务规则。

### 读取说明

* 当前主流程默认不依赖此目录进行业务决策。

### 写入说明

* 除非外部用户明确授权并更新锁定哈希，否则禁止修改任何占位文件。

### 禁止行为

* 禁止将其作为生产流程强依赖。
* 禁止未授权修改占位文件内容。

## CONTRIBMD

### 核心说明

* 多 Agent 协作规范占位目录，当前暂不实现业务流程能力。
* 必须保持基线文件内容完全不变（sha256 强锁定）。

### 命名规则

* 维持占位结构，不纳入业务规则。

### 读取说明

* 当前主流程默认不依赖此目录进行业务决策。

### 写入说明

* 除非外部用户明确授权并更新锁定哈希，否则禁止修改任何占位文件。

### 禁止行为

* 禁止将其作为生产流程强依赖。
* 禁止未授权修改占位文件内容。

## 保护与执行底线

* 受保护文件清单由 `REGISTRYMD` 最新版本定义。
* 默认受保护对象包括：`AGENTS.md`、`MD_SYNTAX_CHECK.md`、所有 `*_TEMPLATE.md`、所有 `*_INDEX.md`、`scripts/md_sync.sh`、`scripts/md_validate.py`、`scripts/md_index_sync.py`、`scripts/check_markdown.sh`。
* 禁止跳过 INDEX 直接写条目。
* 条目模式（entry）按部门细则执行；`ENVIRONMENTMD` 的同一 `Key` 仅允许一个当前有效条目。
* 禁止在更新修正模式（update）覆盖历史版本。
* 禁止在日志模式（log）覆盖历史事件或把多事件混写成单条记录。
* 禁止在正式条目中保留占位词（`TODO`、`TBD`、`[待补充]`）。
* 禁止更新后不执行 `md_sync.sh`。
