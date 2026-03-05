# AGENTSMD

AGENTSMD 是一套“面向 Agent 的项目文档操作系统”。
它通过统一模板、索引、模式约束和校验脚本，让 Agent 在**无长期记忆**前提下，也能稳定完成项目理解、记录与更新。

## 核心能力

- 三种文档模式：
  - `update`：版本流（保留历史，默认读最新）
  - `log`：事件流（按事件追加，不覆盖历史）
  - `entry`：条目流（按 Key 访问，已有 Key 更新原条目）
- 部门化文档结构（SPEC / RESEARCH / DECISION / CHANGE / RUN / ERROR / SECURITY 等）
- 索引驱动访问（先读 INDEX 再读条目）
- 受保护路径管控（由 REGISTRY 约束）
- 自动化校验与索引同步（`scripts/`）
- 本地可视化控制台（树状浏览、编辑、预览、校验同步）

## 目录概览

- `AGENTS.md`：全局合同与工作流
- `MD_SYNTAX_CHECK.md`：机器可读规则源
- `<DEPT>MD/`：部门文档目录（模板、索引、条目）
- `scripts/`：校验、同步、结构检查脚本
- `agentsmd_web/`：本地可视化控制台

## 快速启动（Web 控制台）

在仓库根目录执行：

```bash
bash run_agentsmd_web.sh
```

Windows：

```bat
run_agentsmd_web.bat
```

默认行为：

- 根目录：当前仓库目录
- 备份目录：`backup/`
- 本地端口：`127.0.0.1:34000`（占用则自动递增）

## 校验与同步

```bash
bash scripts/check_markdown.sh
python3 scripts/md_validate.py
python3 scripts/md_index_sync.py
bash scripts/md_sync.sh
```

按部门范围执行：

```bash
bash scripts/md_sync.sh --scope CHANGEMD
```

## 发布建议

1. 先运行 `bash scripts/md_sync.sh` 确保校验通过。
2. 确认 `REGISTRYMD` 的受保护文件列表完整。
3. 检查 `.github/workflows/ci.yml` 是否与当前脚本一致。
4. 再创建发布 tag。

## License

MIT，见 [LICENSE](LICENSE)。
