# KNOWLEDGE_CONCEPT_AGENT_MEMORY_BOUNDARY_2026_03_05_0418

## Metadata

* **修改者：** Codex
* **Type：** CONCEPT
* **Key：** AGENT_MEMORY_BOUNDARY

## Summary

* 定义 record、update、log 三种模式的知识边界与适用场景，减少跨部门混写。

## Source

* SRC-001 | LOCAL_FILE | /aialra/AGENTSMD/AGENTS.md | 模式定义与部门边界规则来源
* SRC-002 | WEB | <https://react-lm.github.io/> | ReAct 方法论来源

## Key Details

* `entry` 模式用于主题知识沉淀，按 `Key` 检索并维护最新条目入口。
* `update` 模式用于版本演进记录，默认读取 `LATEST` 并保留历史。
* `log` 模式用于事件记录，每条事件独立且按时间序列追加。
* 若边界不清晰，容易把运行问题写入知识库，导致后续检索噪声增加。

## Thought

* 当前文档体系需要明确“知识沉淀”和“事件处置”的分工边界，防止条目语义混杂。
* 三模式分离后，Agent 在读取阶段可先按模式筛选，再按 `Key` 精确定位。
* 该条目作为后续部门扩展时的基础概念，可直接复用于模板和工作流说明。

## Action

* 对照 AGENTS 现有模式定义，抽取 entry、update、log 的关键差异点。
* 将差异点转写为可检索知识条目并按 KEY 建立标准命名。
* 更新 KNOWLEDGE_INDEX，确保该条目可被后续流程直接发现。

## Observation

* 条目建成后，模式边界可被快速复用，减少跨部门记录冲突。
* 索引已可直接定位该知识主题，后续只需更新最新版本条目。
* 该概念可直接指导 ERRORMD、RUNMD、KNOWLEDGEMD 的职责划分。
