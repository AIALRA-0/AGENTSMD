from __future__ import annotations

import os
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models import (
    ActionRequest,
    ActionResponse,
    BackupResponse,
    FileContentResponse,
    ProtectedPathsResponse,
    RenderRequest,
    RenderResponse,
    SaveRequest,
    SaveResponse,
    TreeNode,
)
from services.actions import run_index_sync, run_lint, run_md_sync
from services.backup import create_manual_backup
from services.fs_ops import FsGuard
from services.registry_guard import load_protected_paths, match_protected_rules


APP_ROOT = Path(__file__).resolve().parent
DEFAULT_AGENTS_ROOT = APP_ROOT.parent.resolve()
AGENTS_ROOT = Path(os.getenv("AGENTSMD_ROOT", str(DEFAULT_AGENTS_ROOT))).resolve()
BACKUP_ROOT = Path(
    os.getenv("AGENTSMD_BACKUP_ROOT", str((AGENTS_ROOT / "backup").resolve()))
).resolve()

fs = FsGuard(AGENTS_ROOT)

app = FastAPI(title="AGENTSMD Local Console", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(APP_ROOT / "static")), name="static")


def _display_path(path: Path) -> str:
    """Return a publish-safe relative path when possible."""
    try:
        return str(path.resolve().relative_to(AGENTS_ROOT.parent))
    except ValueError:
        try:
            return str(path.resolve().relative_to(AGENTS_ROOT))
        except ValueError:
            return path.name


@app.get("/")
def root() -> FileResponse:
    return FileResponse(APP_ROOT / "static" / "index.html")


@app.get("/api/tree", response_model=TreeNode)
def api_tree() -> TreeNode:
    return TreeNode.model_validate(fs.list_tree())


@app.get("/api/file", response_model=FileContentResponse)
def api_get_file(path: str = Query(..., description="Path relative to AGENTSMD root")) -> FileContentResponse:
    try:
        content = fs.read_markdown(path)
        return FileContentResponse(path=path, content=content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/render", response_model=RenderResponse)
def api_render(req: RenderRequest) -> RenderResponse:
    html = markdown.markdown(
        req.content,
        extensions=["fenced_code", "tables", "toc", "nl2br"],
        output_format="html5",
    )
    return RenderResponse(html=html)


@app.post("/api/file/save", response_model=SaveResponse)
def api_save_file(req: SaveRequest) -> SaveResponse:
    try:
        target = fs.resolve_path(req.path)
        reg_file, patterns = load_protected_paths(AGENTS_ROOT)
        matched = match_protected_rules(target, patterns, AGENTS_ROOT)
        if matched and not req.confirm_protected:
            return SaveResponse(
                saved=False,
                requires_confirmation=True,
                matched_rules=matched,
                message=f"protected file，Need to confirm and save（Rule source: {reg_file.name}）",
            )

        written = fs.write_markdown(req.path, req.content)
        return SaveResponse(saved=True, bytes=written, message="Saved successfully")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/actions/lint", response_model=ActionResponse)
def api_lint() -> ActionResponse:
    res = run_lint(AGENTS_ROOT)
    return ActionResponse(**res)


@app.post("/api/actions/index-sync", response_model=ActionResponse)
def api_index_sync(req: ActionRequest) -> ActionResponse:
    res = run_index_sync(AGENTS_ROOT, req.scope)
    return ActionResponse(**res)


@app.post("/api/actions/md-sync", response_model=ActionResponse)
def api_md_sync(req: ActionRequest) -> ActionResponse:
    res = run_md_sync(AGENTS_ROOT, req.scope)
    return ActionResponse(**res)


@app.post("/api/backup/manual", response_model=BackupResponse)
def api_manual_backup() -> BackupResponse:
    out_path, size_bytes = create_manual_backup(AGENTS_ROOT, BACKUP_ROOT)
    return BackupResponse(ok=True, backup_path=_display_path(out_path), size_bytes=size_bytes)


@app.get("/api/protected-paths", response_model=ProtectedPathsResponse)
def api_protected_paths() -> ProtectedPathsResponse:
    reg_file, patterns = load_protected_paths(AGENTS_ROOT)
    return ProtectedPathsResponse(source_file=_display_path(reg_file), paths=patterns)
