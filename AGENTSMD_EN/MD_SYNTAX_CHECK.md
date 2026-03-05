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
    "forbidden_phrases": ["TODO", "TBD", "[To be added]"],
    "single_line_sections": ["Summary"],
    "update_status_values": ["LATEST", "ARCHIVED"],
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
  "placeholder_departments": ["CONTRIBMD", "GOVERNANCEMD"],
  "departments": {
    "APIMD": {
      "mode": "entry",
      "template": "API_TEMPLATE.md",
      "index": "API_INDEX.md",
      "filename_regex": "^API_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Endpoint", "Usage", "Token Policy", "Quota & Maintenance", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
    },
    "CHANGEMD": {
      "mode": "update",
      "template": "CHANGE_TEMPLATE.md",
      "index": "CHANGE_INDEX.md",
      "filename_regex": "^CHANGE_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "version number"],
      "key_field": "version number",
      "index_columns": ["version number", "file name", "Modifier", "last updated（UTC）", "Status", "Summary"]
    },
    "DECISIONMD": {
      "mode": "update",
      "template": "DECISION_TEMPLATE.md",
      "index": "DECISION_INDEX.md",
      "filename_regex": "^DECISION_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "version number"],
      "key_field": "version number",
      "index_columns": ["version number", "file name", "Modifier", "last updated（UTC）", "Status", "Summary"]
    },
    "ENVIRONMENTMD": {
      "mode": "entry",
      "template": "ENVIRONMENT_TEMPLATE.md",
      "index": "ENVIRONMENT_INDEX.md",
      "filename_regex": "^ENVIRONMENT_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Key"],
      "key_field": "Key",
      "omit_type_column": true,
      "index_columns": ["Key", "file name", "Modifier", "last updated（UTC）", "Summary"]
    },
    "ERRORMD": {
      "mode": "log",
      "template": "ERROR_TEMPLATE.md",
      "index": "ERROR_INDEX.md",
      "filename_regex": "^ERROR_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention"],
      "metadata_required": ["Modifier", "event time（UTC）", "event name（Key）", "Classification", "level", "scope of influence", "Status"],
      "index_columns": ["event time（UTC）", "level", "event name", "file name", "Classification", "Modifier", "Status", "Summary"]
    },
    "KNOWLEDGEMD": {
      "mode": "entry",
      "template": "KNOWLEDGE_TEMPLATE.md",
      "index": "KNOWLEDGE_INDEX.md",
      "filename_regex": "^KNOWLEDGE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Key Details", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
    },
    "REGISTRYMD": {
      "mode": "update",
      "template": "REGISTRY_TEMPLATE.md",
      "index": "REGISTRY_INDEX.md",
      "filename_regex": "^REGISTRY_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Protected Paths", "Approval Rule", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "version number", "last updated（UTC）", "Status"],
      "key_field": "version number",
      "index_columns": ["version number", "file name", "Modifier", "last updated（UTC）", "Status", "Summary"]
    },
    "RESEARCHMD": {
      "mode": "update",
      "template": "RESEARCH_TEMPLATE.md",
      "index": "RESEARCH_INDEX.md",
      "filename_regex": "^RESEARCH_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Source", "Key Details", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "version number"],
      "key_field": "version number",
      "index_columns": ["version number", "file name", "Modifier", "last updated（UTC）", "Status", "Summary"]
    },
    "RESOURCEMD": {
      "mode": "entry",
      "template": "RESOURCE_TEMPLATE.md",
      "index": "RESOURCE_INDEX.md",
      "filename_regex": "^RESOURCE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Resource Path", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
    },
    "RUNMD": {
      "mode": "log",
      "template": "RUN_TEMPLATE.md",
      "index": "RUN_INDEX.md",
      "filename_regex": "^RUN_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention"],
      "metadata_required": ["Modifier", "event time（UTC）", "event name（Key）", "Classification", "level", "scope of influence", "Status"],
      "index_columns": ["event time（UTC）", "level", "event name", "file name", "Classification", "Modifier", "Status", "Summary"]
    },
    "SECURITYMD": {
      "mode": "log",
      "template": "SECURITY_TEMPLATE.md",
      "index": "SECURITY_INDEX.md",
      "filename_regex": "^SECURITY_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Thought", "Action", "Observation", "Root Cause", "Fix", "Prevention", "Linkage"],
      "metadata_required": ["Modifier", "event name（Key）", "Classification", "level", "scope of influence", "Status"],
      "index_columns": ["level", "event name", "file name", "Classification", "Modifier", "Status", "Summary"]
    },
    "SPECMD": {
      "mode": "update",
      "template": "SPEC_TEMPLATE.md",
      "index": "SPEC_INDEX.md",
      "filename_regex": "^SPEC_V\\d+\\.\\d+\\.\\d+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Spec Details", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "version number"],
      "key_field": "version number",
      "index_columns": ["version number", "file name", "Modifier", "last updated（UTC）", "Status", "Summary"]
    },
    "STYLEMD": {
      "mode": "entry",
      "template": "STYLE_TEMPLATE.md",
      "index": "STYLE_INDEX.md",
      "filename_regex": "^STYLE_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Style Details", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
    },
    "TESTMD": {
      "mode": "entry",
      "template": "TEST_TEMPLATE.md",
      "index": "TEST_INDEX.md",
      "filename_regex": "^TEST_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Test Matrix", "Special Requirements", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
    },
    "TOOLMD": {
      "mode": "entry",
      "template": "TOOL_TEMPLATE.md",
      "index": "TOOL_INDEX.md",
      "filename_regex": "^TOOL_[A-Z0-9]+_[A-Z0-9_]+_\\d{4}_\\d{2}_\\d{2}_\\d{4}\\.md$",
      "required_sections": ["Metadata", "Summary", "Tool Details", "Usage", "Maintenance", "Thought", "Action", "Observation"],
      "metadata_required": ["Modifier", "Type", "Key"],
      "key_field": "Key",
      "index_columns": ["Key", "file name", "Classification", "Modifier", "last updated（UTC）", "Summary"]
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
