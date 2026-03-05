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
    "forbidden_phrases": ["TODO", "TBD", "[待补充]"],
    "single_line_sections": ["Summary"],
    "update_status_values": ["LATEST", "ARCHIVED"],
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
  "placeholder_departments": ["CONTRIBMD", "GOVERNANCEMD"],
  "departments": {
    "APIMD": {
      "mode": "entry",
      "template": "API_TEMPLATE.md",
      "index": "API_INDEX.md",
      "filename_regex": "^API_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Endpoint", "Usage", "Token Policy", "Quota & Maintenance", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
    },
    "CHANGEMD": {
      "mode": "update",
      "template": "CHANGE_TEMPLATE.md",
      "index": "CHANGE_INDEX.md",
      "filename_regex": "^CHANGE_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "版本号"],
      "key_field": "版本号",
      "index_columns": ["版本号", "文件名", "修改者", "最后更新（UTC）", "状态", "总结"]
    },
    "DECISIONMD": {
      "mode": "update",
      "template": "DECISION_TEMPLATE.md",
      "index": "DECISION_INDEX.md",
      "filename_regex": "^DECISION_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "版本号"],
      "key_field": "版本号",
      "index_columns": ["版本号", "文件名", "修改者", "最后更新（UTC）", "状态", "总结"]
    },
    "ENVIRONMENTMD": {
      "mode": "entry",
      "template": "ENVIRONMENT_TEMPLATE.md",
      "index": "ENVIRONMENT_INDEX.md",
      "filename_regex": "^ENVIRONMENT_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Key"],
      "key_field": "Key",
      "omit_type_column": true,
      "index_columns": ["Key", "文件名", "修改者", "最后更新（UTC）", "总结"]
    },
    "ERRORMD": {
      "mode": "log",
      "template": "ERROR_TEMPLATE.md",
      "index": "ERROR_INDEX.md",
      "filename_regex": "^ERROR_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention"],
      "metadata_required": ["修改者", "事件时间（UTC）", "事件名（Key）", "分类", "级别", "影响范围", "状态"],
      "index_columns": ["事件时间（UTC）", "级别", "事件名", "文件名", "分类", "修改者", "状态", "总结"]
    },
    "KNOWLEDGEMD": {
      "mode": "entry",
      "template": "KNOWLEDGE_TEMPLATE.md",
      "index": "KNOWLEDGE_INDEX.md",
      "filename_regex": "^KNOWLEDGE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Key Details", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
    },
    "REGISTRYMD": {
      "mode": "update",
      "template": "REGISTRY_TEMPLATE.md",
      "index": "REGISTRY_INDEX.md",
      "filename_regex": "^REGISTRY_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Protected Paths", "Approval Rule", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "版本号", "最后更新（UTC）", "状态"],
      "key_field": "版本号",
      "index_columns": ["版本号", "文件名", "修改者", "最后更新（UTC）", "状态", "总结"]
    },
    "RESEARCHMD": {
      "mode": "update",
      "template": "RESEARCH_TEMPLATE.md",
      "index": "RESEARCH_INDEX.md",
      "filename_regex": "^RESEARCH_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Key Details", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "版本号"],
      "key_field": "版本号",
      "index_columns": ["版本号", "文件名", "修改者", "最后更新（UTC）", "状态", "总结"]
    },
    "RESOURCEMD": {
      "mode": "entry",
      "template": "RESOURCE_TEMPLATE.md",
      "index": "RESOURCE_INDEX.md",
      "filename_regex": "^RESOURCE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Resource Path", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
    },
    "RUNMD": {
      "mode": "log",
      "template": "RUN_TEMPLATE.md",
      "index": "RUN_INDEX.md",
      "filename_regex": "^RUN_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention"],
      "metadata_required": ["修改者", "事件时间（UTC）", "事件名（Key）", "分类", "级别", "影响范围", "状态"],
      "index_columns": ["事件时间（UTC）", "级别", "事件名", "文件名", "分类", "修改者", "状态", "总结"]
    },
    "SECURITYMD": {
      "mode": "log",
      "template": "SECURITY_TEMPLATE.md",
      "index": "SECURITY_INDEX.md",
      "filename_regex": "^SECURITY_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention", "Linkage"],
      "metadata_required": ["修改者", "事件名（Key）", "分类", "级别", "影响范围", "状态"],
      "index_columns": ["级别", "事件名", "文件名", "分类", "修改者", "状态", "总结"]
    },
    "SPECMD": {
      "mode": "update",
      "template": "SPEC_TEMPLATE.md",
      "index": "SPEC_INDEX.md",
      "filename_regex": "^SPEC_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Spec Details", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "版本号"],
      "key_field": "版本号",
      "index_columns": ["版本号", "文件名", "修改者", "最后更新（UTC）", "状态", "总结"]
    },
    "STYLEMD": {
      "mode": "entry",
      "template": "STYLE_TEMPLATE.md",
      "index": "STYLE_INDEX.md",
      "filename_regex": "^STYLE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Style Details", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
    },
    "TESTMD": {
      "mode": "entry",
      "template": "TEST_TEMPLATE.md",
      "index": "TEST_INDEX.md",
      "filename_regex": "^TEST_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Test Matrix", "Special Requirements", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
    },
    "TOOLMD": {
      "mode": "entry",
      "template": "TOOL_TEMPLATE.md",
      "index": "TOOL_INDEX.md",
      "filename_regex": "^TOOL_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Tool Details", "Usage", "Maintenance", "Thought", "Action", "Observation"],
      "metadata_required": ["修改者", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "文件名", "分类", "修改者", "最后更新（UTC）", "总结"]
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
  }
}
```
<!-- MD_RULES_END -->
