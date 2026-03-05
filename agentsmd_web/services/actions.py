from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> dict:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "command": " ".join(shlex.quote(c) for c in cmd),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def run_lint(agents_root: Path) -> dict:
    # Prefer existing shell script on Unix-like systems.
    if os.name != "nt" and (agents_root / "scripts" / "check_markdown.sh").exists():
        return _run(["bash", "scripts/check_markdown.sh"], agents_root)

    # Cross-platform fallback equivalent.
    _run(["npx", "--yes", "markdownlint-cli2", "**/*.md", "--fix"], agents_root)
    return _run(["npx", "--yes", "markdownlint-cli2", "**/*.md"], agents_root)


def run_index_sync(agents_root: Path, scope: str | None = None) -> dict:
    cmd = [sys.executable, "scripts/md_index_sync.py"]
    if scope:
        cmd += ["--scope", scope]
    return _run(cmd, agents_root)


def run_validate(agents_root: Path, scope: str | None = None) -> dict:
    cmd = [sys.executable, "scripts/md_validate.py"]
    if scope:
        cmd += ["--scope", scope]
    return _run(cmd, agents_root)


def run_md_sync(agents_root: Path, scope: str | None = None) -> dict:
    if os.name != "nt" and (agents_root / "scripts" / "md_sync.sh").exists():
        cmd = ["bash", "scripts/md_sync.sh"]
        if scope:
            cmd += ["--scope", scope]
        return _run(cmd, agents_root)

    # Cross-platform fallback equivalent.
    logs = []

    r1 = run_lint(agents_root)
    logs.append(r1)
    if not r1["ok"]:
        return _combine("md_sync (fallback)", logs)

    r2 = run_validate(agents_root, scope)
    logs.append(r2)
    if not r2["ok"]:
        return _combine("md_sync (fallback)", logs)

    r3 = run_index_sync(agents_root, scope)
    logs.append(r3)
    if not r3["ok"]:
        return _combine("md_sync (fallback)", logs)

    r4 = run_validate(agents_root, scope)
    logs.append(r4)
    return _combine("md_sync (fallback)", logs)


def _combine(name: str, logs: list[dict]) -> dict:
    ok = all(x["ok"] for x in logs)
    stdout = "\n\n".join([f"$ {x['command']}\n{x['stdout']}".strip() for x in logs]).strip()
    stderr = "\n\n".join([f"$ {x['command']}\n{x['stderr']}".strip() for x in logs if x["stderr"]]).strip()
    return {
        "ok": ok,
        "command": name,
        "returncode": 0 if ok else 1,
        "stdout": stdout,
        "stderr": stderr,
    }
