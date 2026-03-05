from __future__ import annotations

import fnmatch
import re
from pathlib import Path


def _extract_table_rows(index_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    lines = index_text.splitlines()
    table_started = False
    for i, line in enumerate(lines):
        if line.startswith("|"):
            if not table_started:
                if i + 1 < len(lines) and lines[i + 1].startswith("|") and "---" in lines[i + 1]:
                    table_started = True
                continue
            if "---" in line:
                continue
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cols)
        elif table_started:
            break
    return rows


def latest_registry_file(agents_root: Path) -> Path:
    reg_dir = agents_root / "REGISTRYMD"
    index_path = reg_dir / "REGISTRY_INDEX.md"
    if index_path.exists():
        rows = _extract_table_rows(index_path.read_text(encoding="utf-8"))
        if rows:
            # expected update index: version number | file name | Modifier | last updated（UTC） | Status | Summary
            file_stem = rows[0][1] if len(rows[0]) > 1 else ""
            if file_stem:
                candidate = reg_dir / f"{file_stem}.md"
                if candidate.exists():
                    return candidate

    versions = sorted(reg_dir.glob("REGISTRY_V*.md"), key=lambda p: p.name, reverse=True)
    if not versions:
        raise FileNotFoundError("No REGISTRY version file found")
    return versions[0]


def parse_protected_paths(registry_file: Path) -> list[str]:
    text = registry_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_section = False
    paths: list[str] = []
    for line in lines:
        if line.startswith("## "):
            in_section = line.strip() == "## Protected Paths"
            continue
        if in_section:
            m = re.match(r"^\*\s+(.*)$", line.strip())
            if m:
                value = m.group(1).strip()
                if value:
                    paths.append(value)
    return paths


def load_protected_paths(agents_root: Path) -> tuple[Path, list[str]]:
    reg_file = latest_registry_file(agents_root)
    patterns = parse_protected_paths(reg_file)
    return reg_file, [_normalize_pattern_for_root(p, agents_root) for p in patterns]


def _normalize_pattern_for_root(pattern: str, agents_root: Path) -> str:
    norm = pattern.replace("\\", "/")
    # Keep relative patterns unchanged.
    if not norm.startswith("/"):
        return norm

    # If path already rooted in current AGENTSMD, keep as-is.
    if norm.startswith(agents_root.as_posix()):
        return norm

    # Portability shim: remap absolute patterns containing /AGENTSMD/ to local root.
    marker = "/AGENTSMD/"
    if marker in norm:
        suffix = norm.split(marker, 1)[1]
        return f"{agents_root.as_posix()}/{suffix}"
    if norm.endswith("/AGENTSMD"):
        return agents_root.as_posix()
    return norm


def match_protected_rules(target_file: Path, patterns: list[str], agents_root: Path) -> list[str]:
    target_abs = target_file.resolve().as_posix()
    target_rel = target_file.resolve().relative_to(agents_root.resolve()).as_posix()
    matched: list[str] = []

    for pat in patterns:
        norm = pat.replace("\\", "/")
        if fnmatch.fnmatch(target_abs, norm) or fnmatch.fnmatch(target_rel, norm):
            matched.append(pat)
            continue

        # Support absolute-style patterns rooted at AGENTSMD for relative targets.
        if norm.startswith(agents_root.as_posix()):
            rel_pat = norm[len(agents_root.as_posix()):].lstrip("/")
            if fnmatch.fnmatch(target_rel, rel_pat):
                matched.append(pat)

    return matched
