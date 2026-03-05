# MD Constraint verification rules

## target

* This document is AGENTSMD source of machine rules。
* `scripts/md_validate.py` with `scripts/md_index_sync.py` Only parse the rule block of this file。
* When adding or adjusting departments，Just modify the rule block of this file，No need to modify the script。

## Maintenance instructions

* Rule blocks must be placed in `MD_RULES_START/MD_RULES_END` between markers。
* It is recommended to keep `yaml` code block，Content is available JSON Compatible syntax。
* Must be executed after modifying the rules：`bash scripts/md_sync.sh`。

<!-- MD_RULES_START -->
```yaml

{
  "schema_version": 2,
  "global": {
    "forbidden_phrases": [
      "TODO",
      "TBD",
      "[To be added]"
    ],
    "single_line_sections": [
      "Summary"
    ],
    "update_status_values": [
      "LATEST",
      "ARCHIVED"
    ],
    "source_format": "^SRC-\\d+\\s+\\|\\s+(?:Type\\([A-Z_]+\\)|[A-Z_]+)\\s+\\|\\s+.+\\s+\\|\\s+.+$"
  },
  "active_departments": [
    "APIMD",
    "CHANGEMD",
    "DECISIONMD",
    "ENVIRONMENTMD",
    "ERRORMD",
    "KNOWLEDGEMD",
    "REGISTRYMD",
    "RESEARCHMD",
    "RESOURCEMD",
    "RUNMD",
    "SECURITYMD",
    "SPECMD",
    "STYLEMD",
    "TESTMD",
    "TOOLMD"
  ],
  "placeholder_departments": [
    "CONTRIBMD",
    "GOVERNANCEMD"
  ],
  "departments": {
    "APIMD": {
      "mode": "entry",
      "template": "API_TEMPLATE.md",
      "index": "API_INDEX.md",
      "filename_regex": "^API_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Source",
        "Endpoint",
        "Usage",
        "Token Policy",
        "Quota & Maintenance",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "CHANGEMD": {
      "mode": "update",
      "template": "CHANGE_TEMPLATE.md",
      "index": "CHANGE_INDEX.md",
      "filename_regex": "^CHANGE_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "version number"
      ],
      "key_field": "version number",
      "index_columns": [
        "version number",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Status",
        "Summary"
      ]
    },
    "DECISIONMD": {
      "mode": "update",
      "template": "DECISION_TEMPLATE.md",
      "index": "DECISION_INDEX.md",
      "filename_regex": "^DECISION_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "version number"
      ],
      "key_field": "version number",
      "index_columns": [
        "version number",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Status",
        "Summary"
      ]
    },
    "ENVIRONMENTMD": {
      "mode": "entry",
      "template": "ENVIRONMENT_TEMPLATE.md",
      "index": "ENVIRONMENT_INDEX.md",
      "filename_regex": "^ENVIRONMENT_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Key"
      ],
      "key_field": "Key",
      "omit_type_column": true,
      "index_columns": [
        "Key",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "ERRORMD": {
      "mode": "log",
      "template": "ERROR_TEMPLATE.md",
      "index": "ERROR_INDEX.md",
      "filename_regex": "^ERROR_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation",
        "Root Cause",
        "Fix",
        "Prevention"
      ],
      "metadata_required": [
        "Modifier",
        "event time（UTC）",
        "event name（Key）",
        "Classification",
        "Level",
        "scope of influence",
        "Status"
      ],
      "index_columns": [
        "event time（UTC）",
        "Level",
        "event name",
        "file name",
        "Classification",
        "Modifier",
        "Status",
        "Summary"
      ]
    },
    "KNOWLEDGEMD": {
      "mode": "entry",
      "template": "KNOWLEDGE_TEMPLATE.md",
      "index": "KNOWLEDGE_INDEX.md",
      "filename_regex": "^KNOWLEDGE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Source",
        "Key Details",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "REGISTRYMD": {
      "mode": "update",
      "template": "REGISTRY_TEMPLATE.md",
      "index": "REGISTRY_INDEX.md",
      "filename_regex": "^REGISTRY_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Protected Paths",
        "Approval Rule",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "version number",
        "last updated（UTC）",
        "Status"
      ],
      "key_field": "version number",
      "index_columns": [
        "version number",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Status",
        "Summary"
      ]
    },
    "RESEARCHMD": {
      "mode": "update",
      "template": "RESEARCH_TEMPLATE.md",
      "index": "RESEARCH_INDEX.md",
      "filename_regex": "^RESEARCH_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Source",
        "Key Details",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "version number"
      ],
      "key_field": "version number",
      "index_columns": [
        "version number",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Status",
        "Summary"
      ]
    },
    "RESOURCEMD": {
      "mode": "entry",
      "template": "RESOURCE_TEMPLATE.md",
      "index": "RESOURCE_INDEX.md",
      "filename_regex": "^RESOURCE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Resource Path",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "RUNMD": {
      "mode": "log",
      "template": "RUN_TEMPLATE.md",
      "index": "RUN_INDEX.md",
      "filename_regex": "^RUN_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation",
        "Root Cause",
        "Fix",
        "Prevention"
      ],
      "metadata_required": [
        "Modifier",
        "event time（UTC）",
        "event name（Key）",
        "Classification",
        "Level",
        "scope of influence",
        "Status"
      ],
      "index_columns": [
        "event time（UTC）",
        "Level",
        "event name",
        "file name",
        "Classification",
        "Modifier",
        "Status",
        "Summary"
      ]
    },
    "SECURITYMD": {
      "mode": "log",
      "template": "SECURITY_TEMPLATE.md",
      "index": "SECURITY_INDEX.md",
      "filename_regex": "^SECURITY_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Thought",
        "Action",
        "Observation",
        "Root Cause",
        "Fix",
        "Prevention",
        "Linkage"
      ],
      "metadata_required": [
        "Modifier",
        "event name（Key）",
        "Classification",
        "Level",
        "scope of influence",
        "Status"
      ],
      "index_columns": [
        "Level",
        "event name",
        "file name",
        "Classification",
        "Modifier",
        "Status",
        "Summary"
      ]
    },
    "SPECMD": {
      "mode": "update",
      "template": "SPEC_TEMPLATE.md",
      "index": "SPEC_INDEX.md",
      "filename_regex": "^SPEC_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Spec Details",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "version number"
      ],
      "key_field": "version number",
      "index_columns": [
        "version number",
        "file name",
        "Modifier",
        "last updated（UTC）",
        "Status",
        "Summary"
      ]
    },
    "STYLEMD": {
      "mode": "entry",
      "template": "STYLE_TEMPLATE.md",
      "index": "STYLE_INDEX.md",
      "filename_regex": "^STYLE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Style Details",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "TESTMD": {
      "mode": "entry",
      "template": "TEST_TEMPLATE.md",
      "index": "TEST_INDEX.md",
      "filename_regex": "^TEST_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Test Matrix",
        "Special Requirements",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    },
    "TOOLMD": {
      "mode": "entry",
      "template": "TOOL_TEMPLATE.md",
      "index": "TOOL_INDEX.md",
      "filename_regex": "^TOOL_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": [
        "Metadata",
        "Summary",
        "Tool Details",
        "Usage",
        "Maintenance",
        "Thought",
        "Action",
        "Observation"
      ],
      "metadata_required": [
        "Modifier",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "file name",
        "Classification",
        "Modifier",
        "last updated（UTC）",
        "Summary"
      ]
    }
  },
  "placeholder_lock": {
    "enabled": true,
    "files": [
      {
        "path": "CONTRIBMD/CONTRIB_INDEX.md",
        "sha256": "516758fa79955718a01d90cbb917cb0c39988f92a51dacceed56b3e057fc985d"
      },
      {
        "path": "CONTRIBMD/CONTRIB_TEMPLATE.md",
        "sha256": "9a10b3e4de0215664d528ecb7b6696fe990d966f9c4aadc966b6ce16e90a85d5"
      },
      {
        "path": "CONTRIBMD/CONTRIB_V1.0.0_2026_03_04_1430.md",
        "sha256": "55cf6e0329d895dfbbf53871b9bf939694da7c1ec12295c99ae96bd6a14858f8"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_INDEX.md",
        "sha256": "c8bd5ed57f89345c9e6d70112dc09963cc0d451b21d24b62b6c36b1cbaf8f90d"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_TEMPLATE.md",
        "sha256": "5194ff7e541c721fddf0083e5b29a6f3df5f3accc2dcc77274639accfdf83242"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_V1.0.0_2026_03_04_1430.md",
        "sha256": "8e8f7f3f1607bde184f04228fd0cd95fc1defe8ec3c87fca7d58beb20b13db2c"
      }
    ]
  },
  "workflow_enforcement": {
    "enabled": true,
    "trace_department": "RUNMD",
    "trace_filename_regex": "^RUN_INFO_WORKFLOW_[A-Z0-9_]+_(?:YYYY_MM_DD_HHMM|\\d{4}_\\d{2}_\\d{2}_\\d{4})\\.md$",
    "trace_section": "Workflow Trace",
    "step_status_values": [
      "CHANGED",
      "READ_ONLY",
      "SKIPPED_JUSTIFIED"
    ],
    "step_policy_values": [
      "must_read",
      "must_write",
      "optional_write"
    ],
    "catalog": {
      "PROJECT_INIT": {
        "description": "PROJECT_INIT",
        "steps": [
          {
            "step_id": "S01",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S08",
            "department": "STYLEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S09",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S10",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S11",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S12",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "RULE_CHANGE": {
        "description": "RULE_CHANGE",
        "steps": [
          {
            "step_id": "S01",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "RULE_CONFLICT_FIX": {
        "description": "RULE_CONFLICT_FIX",
        "steps": [
          {
            "step_id": "S01",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S05",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "REQUIREMENT_ANALYSIS": {
        "description": "REQUIREMENT_ANALYSIS",
        "steps": [
          {
            "step_id": "S01",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          }
        ]
      },
      "RESOURCE_KNOWLEDGE_ACCUMULATION": {
        "description": "RESOURCE_KNOWLEDGE_ACCUMULATION",
        "steps": [
          {
            "step_id": "S01",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          }
        ]
      },
      "CODING_IMPLEMENTATION": {
        "description": "CODING_IMPLEMENTATION",
        "steps": [
          {
            "step_id": "S01",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "STYLEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S08",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S09",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "API_INTEGRATION": {
        "description": "API_INTEGRATION",
        "steps": [
          {
            "step_id": "S01",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "API_REPLACE": {
        "description": "API_REPLACE",
        "steps": [
          {
            "step_id": "S01",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S08",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "STRATEGY_MARKET_CORRECTION": {
        "description": "STRATEGY_MARKET_CORRECTION",
        "steps": [
          {
            "step_id": "S01",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "DATA_RESOURCE_CHANGE": {
        "description": "DATA_RESOURCE_CHANGE",
        "steps": [
          {
            "step_id": "S01",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "SPEC_CHANGE": {
        "description": "SPEC_CHANGE",
        "steps": [
          {
            "step_id": "S01",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "BUG_FIX": {
        "description": "BUG_FIX",
        "steps": [
          {
            "step_id": "S01",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S06",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S07",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          }
        ]
      },
      "RUNTIME_TROUBLESHOOT": {
        "description": "RUNTIME_TROUBLESHOOT",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "SECURITY_INCIDENT": {
        "description": "SECURITY_INCIDENT",
        "steps": [
          {
            "step_id": "S01",
            "department": "SECURITYMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S04",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "ENV_CHANGE": {
        "description": "ENV_CHANGE",
        "steps": [
          {
            "step_id": "S01",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S06",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "TOOL_UPGRADE": {
        "description": "TOOL_UPGRADE",
        "steps": [
          {
            "step_id": "S01",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S08",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "DEPENDENCY_UPGRADE": {
        "description": "DEPENDENCY_UPGRADE",
        "steps": [
          {
            "step_id": "S01",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S08",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "AUTH_POLICY_ADJUST": {
        "description": "AUTH_POLICY_ADJUST",
        "steps": [
          {
            "step_id": "S01",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S07",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "PERFORMANCE_OPT": {
        "description": "PERFORMANCE_OPT",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S08",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "STABILITY_HARDENING": {
        "description": "STABILITY_HARDENING",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S08",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "RELEASE_UPDATE": {
        "description": "RELEASE_UPDATE",
        "steps": [
          {
            "step_id": "S01",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S04",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "PRE_RELEASE_GATE": {
        "description": "PRE_RELEASE_GATE",
        "steps": [
          {
            "step_id": "S01",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S04",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S05",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "POST_RELEASE_MONITOR": {
        "description": "POST_RELEASE_MONITOR",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S04",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S08",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S09",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S10",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "EMERGENCY_ROLLBACK": {
        "description": "EMERGENCY_ROLLBACK",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S07",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "POSTMORTEM_KNOWLEDGE": {
        "description": "POSTMORTEM_KNOWLEDGE",
        "steps": [
          {
            "step_id": "S01",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S04",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S08",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          }
        ]
      },
      "PROTECTION_POLICY_UPDATE": {
        "description": "PROTECTION_POLICY_UPDATE",
        "steps": [
          {
            "step_id": "S01",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "DOC_RULE_CORRECTION": {
        "description": "DOC_RULE_CORRECTION",
        "steps": [
          {
            "step_id": "S01",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S03",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      },
      "CROSS_DEPT_REFACTOR": {
        "description": "CROSS_DEPT_REFACTOR",
        "steps": [
          {
            "step_id": "S01",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S06",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S07",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          }
        ]
      },
      "FALLBACK_FLOW": {
        "description": "FALLBACK_FLOW",
        "steps": [
          {
            "step_id": "S01",
            "department": "RESEARCHMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S02",
            "department": "RESOURCEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S03",
            "department": "KNOWLEDGEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S04",
            "department": "SPECMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S05",
            "department": "DECISIONMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S06",
            "department": "APIMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S07",
            "department": "TOOLMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S08",
            "department": "STYLEMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S09",
            "department": "ENVIRONMENTMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S10",
            "department": "REGISTRYMD",
            "policy": "must_read",
            "allow_skip": false
          },
          {
            "step_id": "S11",
            "department": "CHANGEMD",
            "policy": "must_write",
            "allow_skip": false
          },
          {
            "step_id": "S12",
            "department": "TESTMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S13",
            "department": "ERRORMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S14",
            "department": "SECURITYMD",
            "policy": "optional_write",
            "allow_skip": true
          },
          {
            "step_id": "S15",
            "department": "RUNMD",
            "policy": "optional_write",
            "allow_skip": true
          }
        ]
      }
    }
  }
}

```
<!-- MD_RULES_END -->
