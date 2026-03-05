from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class TreeNode(BaseModel):
    name: str
    path: str
    type: Literal["dir", "file"]
    modified_ts: float | None = None
    modified_at: str | None = None
    children: list["TreeNode"] = Field(default_factory=list)


class FileContentResponse(BaseModel):
    path: str
    content: str
    encoding: str = "utf-8"


class RenderRequest(BaseModel):
    content: str


class RenderResponse(BaseModel):
    html: str


class SaveRequest(BaseModel):
    path: str
    content: str
    confirm_protected: bool = False


class SaveResponse(BaseModel):
    saved: bool
    bytes: int | None = None
    requires_confirmation: bool = False
    matched_rules: list[str] = Field(default_factory=list)
    message: str = ""


class ActionRequest(BaseModel):
    scope: str | None = None


class ActionResponse(BaseModel):
    ok: bool
    command: str
    returncode: int
    stdout: str
    stderr: str


class BackupResponse(BaseModel):
    ok: bool
    backup_path: str
    size_bytes: int


class ProtectedPathsResponse(BaseModel):
    source_file: str
    paths: list[str]
