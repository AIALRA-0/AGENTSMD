#!/usr/bin/env python3
"""Install AGENTSMD CI workflow into any host repository.

Usage:
  python3 AGENTSMD_CN/scripts/install_ci_workflow.py --repo-root /path/to/repo
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Host repository root path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing workflow file")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    template = script_dir / "templates" / "agentsmd-ci.yml"
    if not template.exists():
        print(f"[error] missing template: {template}")
        return 2

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print(f"[error] invalid repo root: {repo_root}")
        return 2

    workflow_dir = repo_root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    target = workflow_dir / "agentsmd-ci.yml"

    src = template.read_text(encoding="utf-8")
    if target.exists():
        dst = target.read_text(encoding="utf-8")
        if dst == src:
            print(f"[ok] workflow already up-to-date: {target}")
            return 0
        if not args.force:
            print(f"[error] target exists and differs: {target}")
            print("[hint] re-run with --force to overwrite, or merge manually")
            return 3

    target.write_text(src, encoding="utf-8")
    print(f"[ok] installed workflow: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
