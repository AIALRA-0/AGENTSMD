# AGENTSMD

AGENTSMD It's a set“For Agent project documentation operating system”。
it passes the unified template、Index、Schema constraints and validation scripts，let Agent in**No long-term memory**Under the premise，Can also stably complete project understanding、Record and update。

## core competencies

- Three document modes：
  - `update`：version stream（preserve history，Read latest by default）
  - `log`：event stream（append by event，Do not overwrite history）
  - `entry`：Item stream（press Key visit，Already Key Update original entry）
- Departmental document structure（SPEC / RESEARCH / DECISION / CHANGE / RUN / ERROR / SECURITY Wait）
- Index driven access（Read first INDEX Read the entry again）
- Protected path management（by REGISTRY constraint）
- Automated verification and index synchronization（`scripts/`）
- Local visual console（Tree view、Edit、Preview、Check synchronization）

## Catalog overview

- `AGENTS.md`：Global Contracts and Workflows
- `MD_SYNTAX_CHECK.md`：Machine-readable rule source
- `<DEPT>MD/`：Department document directory（Template、Index、entry）
- `scripts/`：Verify、sync、structure checking script
- `agentsmd_web/`：Local visual console

## quick start（Web console）

Execute in the root directory of the warehouse：

```bash
bash run_agentsmd_web.sh
```

Windows：

```bat
run_agentsmd_web.bat
```

Default behavior：

- root directory：Current warehouse directory
- Backup directory：`backup/`
- local port：`127.0.0.1:34000`（Occupancy is automatically incremented）

## Verification and synchronization

```bash
bash scripts/check_markdown.sh
python3 scripts/md_validate.py
python3 scripts/md_index_sync.py
bash scripts/md_sync.sh
```

Executed according to department scope：

```bash
bash scripts/md_sync.sh --scope CHANGEMD
```

## Post a suggestion

1. Run first `bash scripts/md_sync.sh` Make sure the verification passes。
2. Confirm `REGISTRYMD` Complete list of protected files。
3. Check `.github/workflows/ci.yml` Is it consistent with the current script?。
4. Create a release again tag。

## License

MIT，see [LICENSE](LICENSE)。
