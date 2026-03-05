# MD 约束校验规则

## 目标

* 本文件是 AGENTSMD 的机器规则源。
* `scripts/md_validate.py` 与 `scripts/md_index_sync.py` 仅解析本文件规则块。
* 新增或调整部门时，只需修改本文件规则块，不需要修改脚本。

## 维护说明

* 规则块必须放在 `MD_RULES_START/MD_RULES_END` 标记之间。
* 建议保持 `yaml` 代码块，内容可使用 JSON 兼容语法。
* 修改规则后必须执行：`bash scripts/md_sync.sh`。

<!-- MD_RULES_START -->
```yaml

{
  "schema_version": 2,
  "global": {
    "forbidden_phrases": [
      "TODO",
      "TBD",
      "[待补充]"
    ],
    "single_line_sections": [
      "Summary"
    ],
    "update_status_values": [
      "LATEST",
      "ARCHIVED"
    ],
    "source_format": "^SRC-\\d+\\s+\\|\\s+(?:类型\\([A-Z_]+\\)|[A-Z_]+)\\s+\\|\\s+.+\\s+\\|\\s+.+$"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "版本号"
      ],
      "key_field": "版本号",
      "index_columns": [
        "版本号",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "状态",
        "总结"
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
        "修改者",
        "版本号"
      ],
      "key_field": "版本号",
      "index_columns": [
        "版本号",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "状态",
        "总结"
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
        "修改者",
        "Key"
      ],
      "key_field": "Key",
      "omit_type_column": true,
      "index_columns": [
        "Key",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "事件时间（UTC）",
        "事件名（Key）",
        "分类",
        "级别",
        "影响范围",
        "状态"
      ],
      "index_columns": [
        "事件时间（UTC）",
        "级别",
        "事件名",
        "文件名",
        "分类",
        "修改者",
        "状态",
        "总结"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "版本号",
        "最后更新（UTC）",
        "状态"
      ],
      "key_field": "版本号",
      "index_columns": [
        "版本号",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "状态",
        "总结"
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
        "修改者",
        "版本号"
      ],
      "key_field": "版本号",
      "index_columns": [
        "版本号",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "状态",
        "总结"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "事件时间（UTC）",
        "事件名（Key）",
        "分类",
        "级别",
        "影响范围",
        "状态"
      ],
      "index_columns": [
        "事件时间（UTC）",
        "级别",
        "事件名",
        "文件名",
        "分类",
        "修改者",
        "状态",
        "总结"
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
        "修改者",
        "事件名（Key）",
        "分类",
        "级别",
        "影响范围",
        "状态"
      ],
      "index_columns": [
        "级别",
        "事件名",
        "文件名",
        "分类",
        "修改者",
        "状态",
        "总结"
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
        "修改者",
        "版本号"
      ],
      "key_field": "版本号",
      "index_columns": [
        "版本号",
        "文件名",
        "修改者",
        "最后更新（UTC）",
        "状态",
        "总结"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
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
        "修改者",
        "Type",
        "Key"
      ],
      "key_field": "Key",
      "index_columns": [
        "Key",
        "文件名",
        "分类",
        "修改者",
        "最后更新（UTC）",
        "总结"
      ]
    }
  },
  "placeholder_lock": {
    "enabled": true,
    "files": [
      {
        "path": "CONTRIBMD/CONTRIB_INDEX.md",
        "sha256": "6aedbadea65fb2a8c935829b12526028d1e4e0938299de4d30d07cfd28dd9d82"
      },
      {
        "path": "CONTRIBMD/CONTRIB_TEMPLATE.md",
        "sha256": "9e3a90ebe038568c6026b8a665ea2d155c0159745cfbabfb156eb729dd618e65"
      },
      {
        "path": "CONTRIBMD/CONTRIB_V1.0.0_2026_03_04_1430.md",
        "sha256": "61040d0357fdc6e3d9bacb91afb51a36e0f8717c9d693c22480fdb845b24c1cb"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_INDEX.md",
        "sha256": "10b227e8ce2da372585e4b3fdcda327b8b86c329ecab0785ffcbe604463534dc"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_TEMPLATE.md",
        "sha256": "21a55d6afbeadd4723e5e022ba0e950028e099faf96e45741e9a5b1e76831912"
      },
      {
        "path": "GOVERNANCEMD/GOVERNANCE_V1.0.0_2026_03_04_1430.md",
        "sha256": "94432fcaf898a1c71d82914e0b6f2337bf0f045bfeb43f32e524c14226bd4daa"
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
