# AGENTSMD

## Agent-Native Documentation Operating System

Stateless agents can still work reliably through rules, indexes,
and verifiable workflows.

[![CI](https://github.com/AIALRA-0/AGENTSMD/actions/workflows/agentsmd-ci.yml/badge.svg)](https://github.com/AIALRA-0/AGENTSMD/actions/workflows/agentsmd-ci.yml)
![Bilingual](https://img.shields.io/badge/Bilingual-CN%20%7C%20EN-2563eb)
![Modes](https://img.shields.io/badge/Modes-update%20%7C%20log%20%7C%20entry-0f766e)

[![中文文档](https://img.shields.io/badge/🇨🇳_中文文档-1f2a44?style=for-the-badge)](./AGENTSMD_CN/README.md)
[![English Docs](https://img.shields.io/badge/🇺🇸_English_Docs-1f2a44?style=for-the-badge)](./AGENTSMD_EN/README.md)

---

## Why AGENTSMD

AGENTSMD solves one core problem:
**how to make coding agents reliable without long-term memory**.

Most agent failures come from drift:

- context drift (forgets prior constraints)
- format drift (inconsistent records)
- execution drift (different runs produce different structure)

AGENTSMD turns this into deterministic operations by combining:

1. strict folder contracts
2. index-first access
3. mode-aware writing rules (`update` / `log` / `entry`)
4. automated validation and index synchronization

---

## Architecture

```mermaid
flowchart TD
  A[AGENTS.md Contract] --> B[Department Modes]
  B --> B1[update\nVersion stream]
  B --> B2[log\nEvent stream]
  B --> B3[entry\nKey-based stream]

  B1 --> C[Index-first Read/Write]
  B2 --> C
  B3 --> C

  C --> D[check_markdown.sh]
  D --> E[md_validate.py]
  E --> F[md_index_sync.py]
  F --> G[md_validate.py]

  E --> H[REGISTRY / placeholder_lock]
  H --> I[Protected Paths Gate]
```

### Core Layers

- **Contract Layer**: `AGENTS.md` + `MD_SYNTAX_CHECK.md`
- **Mode Layer**: `update`, `log`, `entry`
- **Department Layer**: SPEC / RESEARCH / DECISION / CHANGE / RUN / ERROR
  / SECURITY / ...
- **Validation Layer**: lint + schema + index consistency
- **Protection Layer**: protected path registry + placeholder lock hashes

---

## Capabilities

- **Index-Driven Access**: agents read index first, then target records.
- **Traceable Evolution**: meaningful changes are captured by mode rules.
- **Deterministic Validation**: write flows end in mandatory checks.
- **Cross-Project Deployability**: AGENTSMD can be dropped into other repos.
- **Bilingual Operations**: CN/EN structures stay aligned.

---

## Potential

AGENTSMD is infrastructure, not just docs:

- for solo builders: company-grade traceability in one-person projects
- for multi-agent teams: shared contracts with lower execution entropy
- for organizations: convert tacit process into verifiable operations

---

## Quick Start

### Validate CN

```bash
cd AGENTSMD_CN
bash scripts/md_sync.sh
```

### Validate EN

```bash
cd AGENTSMD_EN
bash scripts/md_sync.sh
```

### Local Visual Console

```bash
cd AGENTSMD_CN
bash run_agentsmd_web.sh
```

(English mirror is also available under `AGENTSMD_EN`.)

---

## CI and Downstream Integration

This repository includes a root GitHub Actions workflow that:

1. auto-discovers all `AGENTSMD*` directories
2. validates each target with the same 4-step pipeline
3. fails on unsynced index changes

To install the same CI in another repository after dropping AGENTSMD in:

```bash
python3 AGENTSMD_CN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

or

```bash
python3 AGENTSMD_EN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

---

## Screenshots (Placeholders)

Replace these paths with real images when ready.

![Architecture Overview](./AGENTSMD_EN/docs/assets/architecture-overview.png)
![Workflow Pipeline](./AGENTSMD_EN/docs/assets/workflow-pipeline.png)
![Web Console](./AGENTSMD_EN/docs/assets/web-console.png)
![Cross-repo Validation](./AGENTSMD_EN/docs/assets/cross-repo-validation.png)

---

## FAQ

**Q1: Why keep both CN and EN directories?**
A: To keep operational parity while enabling bilingual contributors.

**Q2: Do agents need memory to use this?**
A: No. AGENTSMD is designed for stateless execution.

**Q3: What guarantees consistency?**
A: `check_markdown` + `md_validate` + `md_index_sync` + `md_validate`,
enforced in CI.
