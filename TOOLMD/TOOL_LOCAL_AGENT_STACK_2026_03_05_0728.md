# TOOL_LOCAL_AGENT_STACK_2026_03_05_0728

## Metadata

* **修改者：** Codex
* **Type：** LOCAL
* **Key：** AGENT_STACK

## Summary

* 统一登记本地 Agent 工具栈的路径、调用方式、维护规则与使用边界，支撑日常开发与运维执行。

## Tool Details

* TOOL-001 | Codex CLI | LOCAL | /usr/local/bin/codex | codex | 终端主执行器，用于代码修改、命令执行与流程协作
* TOOL-002 | Python 3 | LOCAL | /usr/bin/python3 | python3 [script.py] | 运行校验脚本、数据处理脚本与自动化工具
* TOOL-003 | Markdown Lint CLI2 | OPEN_SOURCE | /usr/bin/npx | npx markdownlint-cli2 \"**/*.md\" --fix | Markdown 语法检查与自动修复
* TOOL-004 | Git | LOCAL | /usr/bin/git | git [command] | 版本管理与历史追踪
* TOOL-005 | Grep | OPEN_SOURCE | /usr/bin/grep | grep \"pattern\" [path] | 快速检索文件与内容定位

## Usage

* 调用前置条件：执行目录应位于 `/aialra/AGENTSMD` 或其子目录，避免跨项目误操作。
* 最小调用示例：`python3 /aialra/AGENTSMD/scripts/md_validate.py --scope TOOLMD` 用于校验工具部门条目结构。
* 格式检查示例：`npx markdownlint-cli2 \"**/*.md\" --fix`，执行后需复查自动修复结果。
* 索引同步示例：`python3 /aialra/AGENTSMD/scripts/md_index_sync.py --scope TOOLMD`，确保索引与条目一致。
* 输入输出约束：脚本输出失败清单时必须先修复再重试，禁止忽略错误继续推进流程。

## Maintenance

* 维护方式：工具路径和版本由环境维护者定期巡检，条目由执行器按需更新。
* 升级策略：升级工具前先在隔离环境验证兼容性，通过后再更新主环境并刷新 TOOL 条目。
* 回滚策略：升级失败时回滚到上一个稳定版本，并在 CHANGEMD 记录回滚原因与结果。
* 健康检查：每次任务启动前执行核心工具可用性检查（codex/python3/git/grep/npx）。

## Thought

* 工具信息分散会导致执行器重复试错，统一登记可显著减少路径和命令不一致问题。
* 记录“路径+命令+用途”三元信息，能在排障时快速判断是工具缺失还是调用方式错误。
* 将维护策略显式化可降低升级引入的不确定性，避免破坏既有工作流。

## Action

* 按 TOOL 模板重建 `AGENT_STACK` 条目并补齐工具路径、调用示例与维护规则。
* 将本地常用执行工具（codex/python3/git/grep/npx）纳入统一工具栈清单。
* 同步更新 `TOOL_INDEX.md`，将该条目标记为当前有效入口。

## Observation

* 当前条目可直接作为任务执行前的工具检查清单，减少环境差异带来的中断。
* 工具调用与维护规则已结构化沉淀，后续新增工具可按同一格式扩展。
* 与 AGENTS 的 entry 规范一致，可被索引与校验脚本稳定解析。
