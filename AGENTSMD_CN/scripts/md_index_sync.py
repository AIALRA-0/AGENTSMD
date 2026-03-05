#!/usr/bin/env python3
"""
AGENTSMD index synchronizer.

How to extend:
1) Add/modify department definitions in MD_SYNTAX_CHECK.md machine rules block.
2) Keep this script generic; avoid hardcoded department names.
3) Placeholder directories are intentionally excluded from index rewrite.
"""

import argparse
import json
import re
from datetime import datetime
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
    return out


def parse_metadata(lines):
    meta = {}
    pat = re.compile(r"^\*\s+\*\*(.+?)[:：]\*\*\s*(.*)$")
    for ln in lines:
        m = pat.match(ln.strip())
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
    return meta


def parse_summary(lines):
    for ln in lines:
        ln = ln.strip()
        if ln.startswith("* "):
            return ln[2:].strip()
    return "-"


def parse_file_timestamp(stem: str) -> datetime:
    m = re.search(r"_(\d{4})_(\d{2})_(\d{2})_(\d{4})$", stem)
    if not m:
        return datetime.min
    y, mo, d, hm = m.groups()
    hh, mm = hm[:2], hm[2:]
    try:
        return datetime(int(y), int(mo), int(d), int(hh), int(mm))
    except ValueError:
        return datetime.min


def parse_file_timestamp_str(stem: str) -> str:
    dt = parse_file_timestamp(stem)
    if dt == datetime.min:
        return "-"
    return dt.strftime("%Y-%m-%d %H:%M")


def version_tuple(ver: str):
    m = re.match(r"V(\d+)\.(\d+)\.(\d+)", ver or "")
    if not m:
        return (0, 0, 0)
    return tuple(int(x) for x in m.groups())


def render_index(name: str, mode: str, columns, rows):
    if mode == "entry":
        notes = [
            "* 本目录为条目模式（entry），按 Key 读取并维护当前有效条目。",
            "* 同一 Key 仅保留一条索引行；更新时刷新文件名时间戳与最后更新时间。",
        ]
    elif mode == "log":
        notes = [
            "* 本目录为日志模式（log），按事件新增，不覆盖历史事件。",
            "* 索引按事件时间倒序排列，便于优先处理最新事件。",
        ]
    else:
        notes = [
            "* 本目录为更新修正模式（update），历史版本保留，默认只读最新版本。",
            "* 索引只保留当前最新版本一行，状态固定为 LATEST。",
        ]

    out = [f"# {name} INDEX", "", "## 索引说明"] + notes + ["", "## 索引", ""]
    out.append("| " + " | ".join(columns) + " |")
    out.append("| " + " | ".join(["---"] * len(columns)) + " |")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    out.append("")
    return "\n".join(out)


def sync_department(name: str, cfg: dict):
    dept = ROOT / name
    template = cfg["template"]
    index = cfg["index"]
    mode = cfg["mode"]
    cols = cfg["index_columns"]
    key_field = cfg.get("key_field", "")

    entries = []
    for p in sorted(dept.glob("*.md")):
        if p.name in {template, index}:
            continue
        sec = section_map(p.read_text(encoding="utf-8"))
        meta = parse_metadata(sec.get("Metadata", []))
        summary = parse_summary(sec.get("Summary", []))
        stem = p.stem
        updated = parse_file_timestamp_str(stem)
        editor = meta.get("修改者", "-")
        if mode == "entry":
            key = meta.get(key_field, "").strip()
            if not key:
                continue
            cat = meta.get("Type", "-")
            entries.append(
                {
                    "key": key,
                    "row": [key, stem, cat, editor, updated, summary],
                    "dt": parse_file_timestamp(stem),
                }
            )
        elif mode == "log":
            event_time = meta.get("事件时间（UTC）", updated)
            level = meta.get("级别", "-")
            event_name = meta.get("事件名（Key）", "-")
            cat = meta.get("分类", "-")
            status = meta.get("状态", "-")
            if "事件时间（UTC）" in cols:
                row = [event_time, level, event_name, stem, cat, editor, status, summary]
            else:
                row = [level, event_name, stem, cat, editor, status, summary]
            entries.append({"row": row, "dt": parse_file_timestamp(stem)})
        else:
            ver = meta.get("版本号", "").strip()
            if not ver:
                continue
            row = [ver, stem, editor, updated, "LATEST", summary]
            entries.append({"version": ver, "row": row})

    rows = []
    if mode == "entry":
        latest = {}
        for item in entries:
            key = item["key"]
            if key not in latest or item["dt"] > latest[key]["dt"]:
                latest[key] = item
        rows = [latest[k]["row"] for k in sorted(latest.keys())]
        if cfg.get("omit_type_column", False):
            rows = [[r[0], r[1], r[3], r[4], r[5]] for r in rows]
    elif mode == "log":
        entries.sort(key=lambda x: x["dt"], reverse=True)
        rows = [x["row"] for x in entries]
    else:
        if entries:
            latest = max(entries, key=lambda x: version_tuple(x["version"]))
            rows = [latest["row"]]

    text = render_index(name, mode, cols, rows)
    (dept / index).write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="", help="department name, e.g. CHANGEMD")
    args = parser.parse_args()

    rules = load_rules()
    active = set(rules.get("active_departments", []))
    placeholders = set(rules.get("placeholder_departments", []))
    depts = rules.get("departments", {})

    if args.scope:
        if args.scope in placeholders:
            print(f"md_index_sync: skip placeholder scope {args.scope}")
            return
        if args.scope not in active:
            raise SystemExit(f"unknown scope: {args.scope}")
        sync_department(args.scope, depts[args.scope])
        print("md_index_sync: completed")
        return

    for name in sorted(active):
        sync_department(name, depts[name])
    print("md_index_sync: completed")


if __name__ == "__main__":
    main()
