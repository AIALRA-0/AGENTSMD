from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


class FsGuard:
    # Keep tree focused on project markdown artifacts, not runtime environments.
    EXCLUDED_DIR_NAMES = {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".venv_agentsmd_web",
    }

    def __init__(self, root: Path):
        self.root = root.resolve()

    def _ensure_in_root(self, target: Path) -> Path:
        resolved = target.resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise ValueError("Path escapes AGENTSMD root")
        return resolved

    def resolve_path(self, rel_or_abs: str) -> Path:
        candidate = Path(rel_or_abs)
        if candidate.is_absolute():
            target = candidate
        else:
            target = self.root / candidate
        resolved = self._ensure_in_root(target)
        if resolved.suffix.lower() != ".md":
            raise ValueError("Only .md files are allowed")
        return resolved

    def relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.root).as_posix()

    @staticmethod
    def _mtime_info(path: Path) -> tuple[float, str]:
        ts = path.stat().st_mtime
        iso = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        return ts, iso

    def list_tree(self) -> dict:
        def walk(dir_path: Path) -> dict:
            dirs = sorted(
                [
                    p
                    for p in dir_path.iterdir()
                    if p.is_dir() and p.name not in self.EXCLUDED_DIR_NAMES and not p.name.startswith(".")
                ],
                key=lambda p: p.name.lower(),
            )
            files = sorted(
                [p for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() == ".md"],
                key=lambda p: p.name.lower(),
            )
            children: list[dict] = []
            for d in dirs:
                child = walk(d)
                if child["children"]:
                    children.append(child)
            for f in files:
                modified_ts, modified_at = self._mtime_info(f)
                children.append(
                    {
                        "name": f.name,
                        "path": self.relative(f),
                        "type": "file",
                        "modified_ts": modified_ts,
                        "modified_at": modified_at,
                        "children": [],
                    }
                )
            return {
                "name": dir_path.name,
                "path": "." if dir_path == self.root else self.relative(dir_path),
                "type": "dir",
                "modified_ts": None,
                "modified_at": None,
                "children": children,
            }

        return walk(self.root)

    def read_markdown(self, rel_or_abs: str) -> str:
        path = self.resolve_path(rel_or_abs)
        return path.read_text(encoding="utf-8")

    def write_markdown(self, rel_or_abs: str, content: str) -> int:
        path = self.resolve_path(rel_or_abs)
        path.write_text(content, encoding="utf-8")
        return path.stat().st_size
