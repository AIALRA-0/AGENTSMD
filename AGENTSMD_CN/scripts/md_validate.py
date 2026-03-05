#!/usr/bin/env python3
"""
AGENTSMD validator.

How to extend:
1) Only update the machine-readable rules block in MD_SYNTAX_CHECK.md.
2) Do not hardcode department names in this script.
3) If placeholder baselines change, update placeholder_lock.files hashes in MD_SYNTAX_CHECK.md.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_FILE = ROOT / "MD_SYNTAX_CHECK.md"


def load_rules() -> dict:
    text = RULES_FILE.read_text(encoding="utf-8")
    m = re.search(
        r"<!--\s*MD_RULES_START\s*-->\s*```yaml\s*(.*?)\s*```\s*<!--\s*MD_RULES_END\s*-->",
        text,
        re.S,
    )
    if not m:
        raise RuntimeError("MD_SYNTAX_CHECK.md missing machine-readable rules block")
    payload = m.group(1).strip()
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(payload)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return json.loads(payload)


def section_map(text: str):
    lines = text.splitlines()
    idx = []
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            idx.append((ln[3:].strip(), i))
    out = {}
    for p, (name, start) in enumerate(idx):
        end = idx[p + 1][1] if p + 1 < len(idx) else len(lines)
        out[name] = lines[start + 1 : end]
    return out, [n for n, _ in idx]


def parse_metadata(section_lines):
    meta = {}
    pat = re.compile(r"^\*\s+\*\*(.+?)[:：]\*\*\s*(.*)$")
    for ln in section_lines:
        m = pat.match(ln.strip())
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
    return meta


def parse_index_columns(index_path: Path):
    lines = index_path.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("|") and "---" not in ln:
            if i + 1 < len(lines) and lines[i + 1].startswith("|") and "---" in lines[i + 1]:
                return [c.strip() for c in ln.strip().strip("|").split("|")]
    return []


def is_single_line_bullet(section_lines):
    entries = [ln.strip() for ln in section_lines if ln.strip()]
    bullets = [x for x in entries if x.startswith("* ")]
    return len(bullets) == 1


def check_required_sections(sec_map, sec_order, required_sections, prefix):
    errs = []
    last_pos = -1
    for name in required_sections:
        if name not in sec_map:
            errs.append(f"{prefix}: missing section '{name}'")
            continue
        pos = sec_order.index(name)
        if pos < last_pos:
            errs.append(f"{prefix}: section order violation at '{name}'")
        last_pos = pos
    return errs


def check_metadata_required(meta, expected, prefix):
    errs = []
    for key in expected:
        if not meta.get(key, "").strip():
            errs.append(f"{prefix}: missing metadata '{key}'")
    return errs


def parse_summary(section_lines):
    for ln in section_lines:
        ln = ln.strip()
        if ln.startswith("* "):
            return ln[2:].strip()
    return ""


def check_source_format(sec_map, file_label, source_regex):
    errs = []
    if "Source" not in sec_map:
        return errs
    rex = re.compile(source_regex)
    for ln in sec_map["Source"]:
        raw = ln.strip()
        if not raw:
            continue
        if not raw.startswith("* "):
            continue
        content = raw[2:].strip()
        if not rex.match(content):
            errs.append(f"{file_label}: Source line format invalid -> {content}")
    return errs


def validate_tool_paths(sec_map, file_label):
    errs = []
    if "Tool Details" not in sec_map:
        return errs
    for ln in sec_map["Tool Details"]:
        raw = ln.strip()
        if not raw.startswith("* "):
            continue
        cols = [c.strip() for c in raw[2:].split("|")]
        if len(cols) < 4:
            continue
        path = cols[3]
        if path.startswith("/") and not Path(path).exists():
            errs.append(f"{file_label}: invalid tool path -> {path}")
    return errs


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_placeholder_lock(rules: dict, skip_lock: bool):
    if skip_lock:
        return []
    lock = rules.get("placeholder_lock", {})
    if not lock.get("enabled", False):
        return []
    errs = []
    for item in lock.get("files", []):
        rel = item.get("path", "").strip()
        expect = item.get("sha256", "").strip().lower()
        if not rel or not expect:
            errs.append("placeholder_lock: invalid lock item")
            continue
        target = ROOT / rel
        if not target.exists():
            errs.append(f"placeholder_lock: missing {rel}")
            continue
        actual = sha256_file(target).lower()
        if actual != expect:
            errs.append(
                f"placeholder_lock: hash mismatch {rel} expected={expect} actual={actual}"
            )
    return errs


def validate_department(name: str, cfg: dict, global_cfg: dict):
    errs = []
    dept = ROOT / name
    if not dept.exists():
        errs.append(f"{name}: directory missing")
        return errs

    template = dept / cfg["template"]
    index = dept / cfg["index"]
    if not template.exists():
        errs.append(f"{name}: template missing {cfg['template']}")
    if not index.exists():
        errs.append(f"{name}: index missing {cfg['index']}")

    expected_cols = cfg["index_columns"]
    if index.exists():
        cols = parse_index_columns(index)
        if cols != expected_cols:
            errs.append(f"{name}: index columns mismatch: {cols} != {expected_cols}")

    rex = re.compile(cfg["filename_regex"])
    req_sections = cfg["required_sections"]
    placeholders = global_cfg.get("forbidden_phrases", [])
    single_line_sections = global_cfg.get("single_line_sections", ["Summary"])
    update_status_values = set(global_cfg.get("update_status_values", ["LATEST", "ARCHIVED"]))
    source_regex = global_cfg.get(
        "source_format",
        r"^SRC-\d+\s+\|\s+[A-Z_]+\s+\|\s+.+\s+\|\s+.+$",
    )

    if template.exists():
        template_text = template.read_text(encoding="utf-8")
        tpl_map, tpl_order = section_map(template_text)
        errs.extend(
            check_required_sections(tpl_map, tpl_order, req_sections, f"{name}: template")
        )
        tpl_meta = parse_metadata(tpl_map.get("Metadata", []))
        errs.extend(
            check_metadata_required(
                tpl_meta, cfg.get("metadata_required", []), f"{name}: template"
            )
        )

    seen = set()
    key_field = cfg.get("key_field", "")
    for p in sorted(dept.glob("*.md")):
        if p.name in {cfg["template"], cfg["index"]}:
            continue
        if not rex.match(p.name):
            errs.append(f"{name}: filename mismatch {p.name}")
        text = p.read_text(encoding="utf-8")
        for phrase in placeholders:
            if phrase and phrase in text:
                errs.append(f"{name}: forbidden phrase '{phrase}' in {p.name}")
        sec_map, sec_order = section_map(text)
        errs.extend(check_required_sections(sec_map, sec_order, req_sections, f"{name}: {p.name}"))
        for sec_name in single_line_sections:
            if sec_name in sec_map and not is_single_line_bullet(sec_map[sec_name]):
                errs.append(f"{name}: {sec_name} must be single bullet line in {p.name}")
        meta = parse_metadata(sec_map.get("Metadata", []))
        errs.extend(
            check_metadata_required(meta, cfg.get("metadata_required", []), f"{name}: {p.name}")
        )
        errs.extend(check_source_format(sec_map, f"{name}: {p.name}", source_regex))
        if name == "TOOLMD":
            errs.extend(validate_tool_paths(sec_map, f"{name}: {p.name}"))

        if key_field:
            val = meta.get(key_field, "").strip()
            if not val:
                errs.append(f"{name}: missing Metadata '{key_field}' in {p.name}")
            elif val in seen:
                errs.append(f"{name}: duplicate {key_field} '{val}'")
            else:
                seen.add(val)
        if cfg.get("mode") == "update":
            status = meta.get("状态", "").strip()
            if status and status not in update_status_values:
                errs.append(f"{name}: invalid 状态 '{status}' in {p.name}")
    return errs


def run_index_sync(scope: str) -> tuple[int, str]:
    cmd = [sys.executable, str(ROOT / "scripts" / "md_index_sync.py"), "--scope", scope]
    p = subprocess.run(cmd, capture_output=True, text=True)
    output = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    return p.returncode, output.strip()


def validate_once(rules: dict, scope: str, skip_placeholder_lock: bool) -> list[str]:
    depts = rules.get("departments", {})
    active_depts = set(rules.get("active_departments", []))
    errs: list[str] = []

    errs.extend(validate_placeholder_lock(rules, skip_placeholder_lock))

    if scope:
        if scope in active_depts:
            errs.extend(validate_department(scope, depts.get(scope, {}), rules.get("global", {})))
        elif scope in set(rules.get("placeholder_departments", [])):
            # Placeholder scope only runs lock checks.
            pass
        else:
            errs.append(f"unknown scope: {scope}")
    else:
        for name in sorted(active_depts):
            errs.extend(validate_department(name, depts.get(name, {}), rules.get("global", {})))
    return errs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="", help="department name, e.g. CHANGEMD")
    parser.add_argument(
        "--skip-placeholder-lock",
        action="store_true",
        help="skip strict sha256 checks for placeholder directories",
    )
    parser.add_argument(
        "--auto-fix-index",
        action="store_true",
        help="auto-run md_index_sync for departments with index columns mismatch, then re-validate",
    )
    args = parser.parse_args()

    rules = load_rules()
    errs = validate_once(rules, args.scope, args.skip_placeholder_lock)

    if args.auto_fix_index and errs:
        mismatch_prefix = "index columns mismatch:"
        fix_scopes: set[str] = set()
        if args.scope:
            if any(mismatch_prefix in e for e in errs):
                fix_scopes.add(args.scope)
        else:
            for e in errs:
                if mismatch_prefix in e and ":" in e:
                    dept = e.split(":", 1)[0].strip()
                    if dept:
                        fix_scopes.add(dept)

        for dept in sorted(fix_scopes):
            code, output = run_index_sync(dept)
            if code != 0:
                errs.append(f"auto-fix index failed for {dept}: {output}")
            else:
                print(f"auto-fix index: {dept}")

        if fix_scopes:
            # Re-run once after auto-fix.
            errs = validate_once(rules, args.scope, args.skip_placeholder_lock)

    if errs:
        print("MD VALIDATION FAILED")
        for e in errs:
            print(f"- {e}")
        sys.exit(1)

    print("md_validate: passed")


if __name__ == "__main__":
    main()
