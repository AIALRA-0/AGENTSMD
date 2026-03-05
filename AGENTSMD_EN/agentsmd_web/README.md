# AGENTSMD Local visual console

This tool is used for local browsing、Edit、Preview `AGENTSMD` under the directory Markdown File，And supports one-click syntax checking、Index updates and full link synchronization。

## Function

- File tree display（dynamic scan，Compatible with new departments）
- Markdown View/Edit/Format preview
- day/Night mode switch（local memory）
- Protected path access before saving（hit REGISTRY Rules need to be confirmed）
- One click execution：Grammar check / Index update / Full link synchronization
- Manual full backup（Default save to `AGENTSMD/backup`）

## One click start

### Linux / macOS

```bash
bash ../run_agentsmd_web.sh
```

### Windows

Double click `..\run_agentsmd_web.bat`，Or execute in terminal：

```bat
..\run_agentsmd_web.bat
```

## Default configuration

- AGENTSMD root directory：`<The directory where the startup script is located>`
- Backup directory：`<AGENTSMDroot directory>/backup`
- local address：`http://127.0.0.1:34000`（If occupied, the port will be automatically incremented.）

Can be overridden through environment variables：

- `AGENTSMD_ROOT`
- `AGENTSMD_BACKUP_ROOT`

## API Short form

- `GET /api/tree`
- `GET /api/file?path=...`
- `POST /api/render`
- `POST /api/file/save`
- `POST /api/actions/lint`
- `POST /api/actions/index-sync`
- `POST /api/actions/md-sync`
- `POST /api/backup/manual`
- `GET /api/protected-paths`

## Troubleshooting

- Startup failed：Check Python Version（>=3.10）
- Grammar check failed：View page“execution log”output
- Save blocked：Description hit protected path，Confirm and save
- Port conflict：The script will automatically switch to an available port
