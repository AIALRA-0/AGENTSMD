#!/usr/bin/env python3
"""
Normalize markdown blank lines safely.

Rules:
- Only process .md files.
- Collapse consecutive blank lines to a single blank line.
- Keep fenced code blocks untouched.

Usage:
  python normalize_blank_lines.py
  python normalize_blank_lines.py --scope CHANGEMD
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def iter_md_files(scope: str) -> list[Path]:
    if scope:
        base = ROOT / scope
        if not base.exists() or not base.is_dir():
            raise SystemExit(f"unknown scope: {scope}")
        return sorted(base.rglob("*.md"))
    return sorted(ROOT.rglob("*.md"))


def normalize_text(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    prev_blank = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            prev_blank = False
            continue

        if in_fence:
            out.append(line)
            prev_blank = False
            continue

        is_blank = stripped == ""
        if is_blank and prev_blank:
            # Skip repeated blank line outside code fences.
            continue

        out.append(line)
        prev_blank = is_blank

    result = "\n".join(out)
    if text.endswith("\n"):
        result += "\n"
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="", help="department name, e.g. CHANGEMD")
    args = parser.parse_args()

    changed = 0
    for path in iter_md_files(args.scope):
        original = path.read_text(encoding="utf-8")
        normalized = normalize_text(original)
        if normalized != original:
            path.write_text(normalized, encoding="utf-8")
            changed += 1

    print(f"normalize_blank_lines: completed (changed={changed})")


if __name__ == "__main__":
    main()
