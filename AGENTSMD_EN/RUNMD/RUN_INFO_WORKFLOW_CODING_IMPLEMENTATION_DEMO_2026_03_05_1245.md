# RUN_INFO_WORKFLOW_CODING_IMPLEMENTATION_DEMO_2026_03_05_1245

## Metadata

* **Modifier：** Codex
* **event time（UTC）：** 2026-03-05 12:45
* **event name（Key）：** WORKFLOW_CODING_IMPLEMENTATION_DEMO
* **Classification：** OBSERVABILITY
* **Level：** INFO
* **scope of influence：** AGENTSMD_EN workflow trace example
* **Status：** RESOLVED

## Summary

* Added a standard Workflow Trace example for coding implementation flow, including binding, step evidence, and machine-readable structure.

## Thought

* Workflow guard requires a RUN_INFO_WORKFLOW trace file to verify process compliance.
* A concrete example lowers onboarding friction and prevents format drift in future tasks.
* This entry is a reusable template sample, not a production incident record.

## Action

* Added one RUNMD example file using `RUN_INFO_WORKFLOW_*` naming.
* Wrote a complete `Workflow Trace` JSON payload with `workflow_id/task_id/reason/steps`.
* Filled every step with `status/evidence/note` fields across must_read/must_write/optional_write patterns.
* Synced `RUN_INDEX.md` so the sample is discoverable by key.

## Observation

* The file can be detected by workflow guard as a valid trace candidate.
* The JSON schema aligns with machine rules and can be copied for real tasks.
* This sample is intentionally documentation-oriented and does not represent a real deployment execution.

## Workflow Trace

```json
{
  "workflow_id": "CODING_IMPLEMENTATION",
  "task_id": "T20260305-DEMO-001",
  "reason": "This task demonstrates the standard trace format for coding implementation workflow.",
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
      "note": "Historical change entry is referenced only to illustrate must_write formatting."
    },
    {
      "step_id": "S09",
      "department": "TESTMD",
      "status": "SKIPPED_JUSTIFIED",
      "evidence": [],
      "note": "This is a documentation sample task; no executable target is changed."
    }
  ]
}
```

## Root Cause

* RUNMD had runtime incident samples but no canonical workflow-trace sample for enforcement onboarding.

## Fix

* Added a dedicated workflow trace sample with complete required fields and realistic step structure.

## Prevention

* For every new workflow type, add at least one concrete sample entry together with rule updates.
