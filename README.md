# AGENTSMD

[![CI](https://github.com/AIALRA-0/AGENTSMD/actions/workflows/agentsmd-ci.yml/badge.svg)](https://github.com/AIALRA-0/AGENTSMD/actions/workflows/agentsmd-ci.yml)
![Bilingual](https://img.shields.io/badge/Bilingual-CN%20%7C%20EN-2563eb)
![Modes](https://img.shields.io/badge/Modes-update%20%7C%20log%20%7C%20entry-0f766e)

[![中文文档](https://img.shields.io/badge/🇨🇳_中文文档-1f2a44?style=for-the-badge)](./AGENTSMD_CN/README.md)
[![English Docs](https://img.shields.io/badge/🇺🇸_English_Docs-1f2a44?style=for-the-badge)](./AGENTSMD_EN/README.md)

## Language Navigation

- [English](#english)
- [中文](#中文)

---

## English

### Agent-Native Documentation Operating System

Stateless agents can still work reliably through rules, indexes,
and verifiable workflows.

### Table of Contents

- [Why AGENTSMD](#why-agentsmd)
- [Architecture](#architecture)
- [Capabilities](#capabilities)
- [Potential](#potential)
- [Quick Start](#quick-start)
- [CI and Downstream Usage](#ci-and-downstream-usage)
- [Screenshots Placeholders](#screenshots-placeholders)
- [FAQ](#faq)

### Why AGENTSMD

AGENTSMD solves one core problem:
**how to make coding agents reliable without long-term memory**.

Most agent failures come from drift:

- Context drift (forgets prior constraints)
- Format drift (inconsistent records)
- Execution drift (different runs produce different structure)

### Architecture

```mermaid
flowchart TD
  A[AGENTS.md Contract] --> B[Department Modes]
  B --> B1[update<br/>Version stream]
  B --> B2[log<br/>Event stream]
  B --> B3[entry<br/>Key-based stream]

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

#### Core Layers

- **Contract Layer**: `AGENTS.md` + rules file
- **Mode Layer**: `update`, `log`, `entry`
- **Department Layer**: SPEC / RESEARCH / DECISION / CHANGE / RUN / ERROR
  / SECURITY / ...
- **Validation Layer**: lint + schema + index consistency
- **Protection Layer**: protected path registry + placeholder lock hashes

### Capabilities

- **Index-driven access**: read index first, then target records.
- **Traceable evolution**: meaningful changes are captured by mode rules.
- **Deterministic validation**: write flows end in mandatory checks.
- **Cross-project deployability**: AGENTSMD can be dropped into other repositories.
- **Bilingual operations**: CN/EN structures stay aligned.

### Potential

AGENTSMD is infrastructure, not just docs.

- For solo builders: company-grade traceability
- For multi-agent teams: shared contracts, lower entropy
- For organizations: tacit process -> verifiable operations

### Quick Start

#### Validate CN

```bash
cd AGENTSMD_CN
bash scripts/md_sync.sh
```

#### Validate EN

```bash
cd AGENTSMD_EN
bash scripts/md_sync.sh
```

#### Local Visual Console

```bash
cd AGENTSMD_CN
bash run_agentsmd_web.sh
```

An English mirror is available under `AGENTSMD_EN`.

### CI and Downstream Usage

The root workflow auto-discovers every `AGENTSMD*` directory and runs:

1. `check_markdown.sh`
2. `md_validate.py`
3. `md_index_sync.py`
4. `md_validate.py`

Install this CI into another repository:

```bash
python3 AGENTSMD_CN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

or

```bash
python3 AGENTSMD_EN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

### Screenshots Placeholders

Replace these paths with real images when ready.

![Architecture Overview](./AGENTSMD_EN/docs/assets/architecture-overview.png)
![Workflow Pipeline](./AGENTSMD_EN/docs/assets/workflow-pipeline.png)
![Web Console](./AGENTSMD_EN/docs/assets/web-console.png)
![Cross-repo Validation](./AGENTSMD_EN/docs/assets/cross-repo-validation.png)

### FAQ

**Q: Why keep both CN and EN directories?**

A: To keep operational parity while enabling bilingual contributors.

[Back to language navigation](#language-navigation)

---

## 中文

### 面向 Agent 的文档操作系统

无长期记忆的 Agent，也能依靠规则、索引和可验证流程稳定工作。

### 目录

- [项目初衷](#项目初衷)
- [架构](#架构)
- [能力](#能力)
- [潜力](#潜力)
- [快速开始](#快速开始)
- [CI 与下放接入](#ci-与下放接入)
- [图片占位](#图片占位)
- [常见问题](#常见问题)

### 项目初衷

AGENTSMD 解决一个核心问题：**如何让无长期记忆的编码 Agent 也能稳定执行**。

常见失败来自三类漂移：

- 上下文漂移（忘约束）
- 格式漂移（记录不一致）
- 执行漂移（同任务输出结构不一致）

### 架构

```mermaid
flowchart TD
  A[AGENTS.md 合同] --> B[部门模式]
  B --> B1[update<br/>版本流]
  B --> B2[log<br/>事件流]
  B --> B3[entry<br/>按 Key 条目流]

  B1 --> C[先索引后读写]
  B2 --> C
  B3 --> C

  C --> D[check_markdown.sh]
  D --> E[md_validate.py]
  E --> F[md_index_sync.py]
  F --> G[md_validate.py]

  E --> H[REGISTRY / placeholder_lock]
  H --> I[受保护路径闸门]
```

#### 核心层次

- **合同层**：`AGENTS.md` + 规则文件
- **模式层**：`update`、`log`、`entry`
- **部门层**：SPEC / RESEARCH / DECISION / CHANGE / RUN / ERROR / SECURITY / ...
- **校验层**：lint + 结构校验 + 索引一致性
- **保护层**：受保护路径清单 + 占位目录哈希锁

### 能力

- **索引驱动访问**：先读索引，再读条目。
- **可追溯演进**：关键修改受模式规则约束并可追踪。
- **确定性校验**：每次写入都以强制校验闭环结束。
- **可下放到任意项目**：AGENTSMD 可以直接接入其他仓库。
- **双语协作**：CN/EN 结构保持同构。

### 潜力

AGENTSMD 是基础设施，不只是文档。

- 对个人：获得公司级可追溯能力
- 对多 Agent：共享契约、降低执行熵
- 对组织：把隐性流程转成可验证操作

### 快速开始

#### 校验中文目录

```bash
cd AGENTSMD_CN
bash scripts/md_sync.sh
```

#### 校验英文目录

```bash
cd AGENTSMD_EN
bash scripts/md_sync.sh
```

#### 启动本地可视化控制台

```bash
cd AGENTSMD_CN
bash run_agentsmd_web.sh
```

英文镜像目录位于 `AGENTSMD_EN`。

### CI 与下放接入

根目录 workflow 会自动发现所有 `AGENTSMD*` 目录，并执行以下链路：

1. `check_markdown.sh`
2. `md_validate.py`
3. `md_index_sync.py`
4. `md_validate.py`

把该 CI 安装到其他仓库：

```bash
python3 AGENTSMD_CN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

或

```bash
python3 AGENTSMD_EN/scripts/install_ci_workflow.py \
  --repo-root /path/to/target-repo
```

### 图片占位

后续把占位图替换为真实截图即可。

![架构总览](./AGENTSMD_EN/docs/assets/architecture-overview.png)
![工作流管线](./AGENTSMD_EN/docs/assets/workflow-pipeline.png)
![Web 控制台](./AGENTSMD_EN/docs/assets/web-console.png)
![跨仓库校验](./AGENTSMD_EN/docs/assets/cross-repo-validation.png)

### 常见问题

**问：为什么保留 CN 与 EN 两套目录？**

答：保证双语协作时仍能保持同构与同规则运行。

[返回语言导航](#language-navigation)
