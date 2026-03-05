# AGENTSMD 本地可视化控制台

本工具用于本地浏览、编辑、预览 `AGENTSMD` 目录下的 Markdown 文件，并支持一键执行语法检查、索引更新和全链路同步。

## 功能

- 文件树展示（动态扫描，兼容新增部门）
- Markdown 查看/编辑/格式化预览
- 日/夜模式切换（本地记忆）
- 保存前受保护路径门禁（命中 REGISTRY 规则需确认）
- 一键执行：语法检查 / 索引更新 / 全链路同步
- 手动全量备份（默认保存到 `AGENTSMD/backup`）

## 一键启动

### Linux / macOS

```bash
bash ../run_agentsmd_web.sh
```

### Windows

双击 `..\run_agentsmd_web.bat`，或在终端执行：

```bat
..\run_agentsmd_web.bat
```

## 默认配置

- AGENTSMD 根目录：`<启动脚本所在目录>`
- 备份目录：`<AGENTSMD根目录>/backup`
- 本地地址：`http://127.0.0.1:34000`（若占用会自动递增端口）

可通过环境变量覆盖：

- `AGENTSMD_ROOT`
- `AGENTSMD_BACKUP_ROOT`

## API 简表

- `GET /api/tree`
- `GET /api/file?path=...`
- `POST /api/render`
- `POST /api/file/save`
- `POST /api/actions/lint`
- `POST /api/actions/index-sync`
- `POST /api/actions/md-sync`
- `POST /api/backup/manual`
- `GET /api/protected-paths`

## 故障排查

- 启动失败：检查 Python 版本（>=3.10）
- 语法检查失败：查看页面“执行日志”输出
- 保存被拦截：说明命中受保护路径，确认后再保存
- 端口冲突：脚本会自动切换到可用端口
