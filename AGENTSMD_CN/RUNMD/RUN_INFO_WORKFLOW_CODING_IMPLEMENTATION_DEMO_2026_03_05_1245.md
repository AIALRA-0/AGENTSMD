# RUN_INFO_WORKFLOW_CODING_IMPLEMENTATION_DEMO_2026_03_05_1245

## Metadata

* **修改者：** Codex
* **事件时间（UTC）：** 2026-03-05 12:45
* **事件名（Key）：** WORKFLOW_CODING_IMPLEMENTATION_DEMO
* **分类：** OBSERVABILITY
* **级别：** INFO
* **影响范围：** AGENTSMD_CN 文档工作流样例
* **状态：** RESOLVED

## Summary

* 为编码实施流程新增标准 Workflow Trace 示例，覆盖工作流绑定、步骤留痕与证据字段格式。

## Thought

* 工作流守卫脚本依赖 RUN_INFO_WORKFLOW 记录才能校验“是否按流程执行”，缺少样例会提高新用户接入成本。
* 示例应严格对齐机读规则字段，确保后续任务可直接复制并替换业务内容。
* 本条目标是提供最小可复用模板，而不是替代真实业务执行记录。

## Action

* 按 RUNMD 规范新增 `RUN_INFO_WORKFLOW_*` 命名的标准记录文件。
* 在 `Workflow Trace` 中写入 `workflow_id/task_id/reason/steps` 的完整 JSON 结构。
* 为每个步骤补齐 `status/evidence/note` 字段，覆盖 must_read、must_write、optional_write 三类策略。
* 同步更新 `RUN_INDEX.md` 索引，确保可通过事件名快速检索该示例。

## Observation

* 示例记录可被工作流守卫正确识别为 trace 文件类型。
* JSON 结构与字段命名与机读规则一致，可直接作为后续任务的复制模板。
* 该示例用于演示流程约束，不代表一次完整的真实业务发布执行。

## Workflow Trace

```json
{
  "workflow_id": "CODING_IMPLEMENTATION",
  "task_id": "T20260305-DEMO-001",
  "reason": "本任务用于演示编码实施工作流的标准留痕格式与字段要求。",
  "steps": [
    {
      "step_id": "S01",
      "department": "SPECMD",
      "status": "READ_ONLY",
      "evidence": [
        "SPECMD/SPEC_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S02",
      "department": "STYLEMD",
      "status": "READ_ONLY",
      "evidence": [
        "STYLEMD/STYLE_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S03",
      "department": "DECISIONMD",
      "status": "READ_ONLY",
      "evidence": [
        "DECISIONMD/DECISION_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S04",
      "department": "TOOLMD",
      "status": "READ_ONLY",
      "evidence": [
        "TOOLMD/TOOL_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S05",
      "department": "APIMD",
      "status": "READ_ONLY",
      "evidence": [
        "APIMD/API_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S06",
      "department": "RESOURCEMD",
      "status": "READ_ONLY",
      "evidence": [
        "RESOURCEMD/RESOURCE_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S07",
      "department": "REGISTRYMD",
      "status": "READ_ONLY",
      "evidence": [
        "REGISTRYMD/REGISTRY_INDEX.md"
      ],
      "note": ""
    },
    {
      "step_id": "S08",
      "department": "CHANGEMD",
      "status": "CHANGED",
      "evidence": [
        "CHANGEMD/CHANGE_V1.0.0_2026_03_05_0235.md"
      ],
      "note": "示例引用历史变更条目用于演示 must_write 字段写法。"
    },
    {
      "step_id": "S09",
      "department": "TESTMD",
      "status": "SKIPPED_JUSTIFIED",
      "evidence": [],
      "note": "本条为文档示例任务，不涉及代码与可执行对象，测试步骤按规则允许跳过。"
    }
  ]
}
```

## Root Cause

* 原有 RUNMD 仅覆盖运行事件样例，缺少 workflow 绑定的标准示例，导致执行规范可读性不足。

## Fix

* 新增标准 workflow trace 示例条目并固化字段结构，作为后续任务参考基线。

## Prevention

* 后续新增工作流时，同步提供至少一条可运行示例，避免规则可用性仅停留在文档描述层。
