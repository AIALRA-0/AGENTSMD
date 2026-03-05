#!/usr/bin/env python3
"""Workflow guard for AGENTSMD.

Purpose:
- Enforce explicit workflow selection via RUN workflow-trace entries.
- Validate step completeness and step policy against machine rules.
- Support strict local gate and report-only CI feedback.

How to extend:
1) Update workflow_enforcement in MD_SYNTAX_CHECK.md.
2) Do not hardcode workflow IDs or department names in this script.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RULES_FILE = ROOT / "MD_SYNTAX_CHECK.md"
REPORT_JSON = ROOT / "workflow_guard_report.json"
REPORT_MD = ROOT / "workflow_guard_report.md"


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


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    return p.returncode, out.strip()


def git_changed_files(base_ref: str | None, head_ref: str | None) -> list[str]:
    if base_ref and head_ref:
        code, out = run(["git", "diff", "--name-only", f"{base_ref}...{head_ref}"])
        if code != 0:
            return []
        return sorted({x.strip() for x in out.splitlines() if x.strip()})

    changed = set()
    for cmd in (
        ["git", "diff", "--name-only"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        code, out = run(cmd)
        if code == 0:
            changed |= {x.strip() for x in out.splitlines() if x.strip()}
    return sorted(changed)


def section_body(markdown_text: str, section_name: str) -> str:
    lines = markdown_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == f"## {section_name}":
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def parse_trace_json(section_text: str) -> dict[str, Any] | None:
    # First preference: fenced json block
    m = re.search(r"```json\s*(\{.*?\})\s*```", section_text, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # Fallback: first object-looking block
    m2 = re.search(r"(\{[\s\S]*\})", section_text)
    if m2:
        try:
            data = json.loads(m2.group(1))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return None


def path_department(path: str, active: set[str], placeholders: set[str]) -> str | None:
    p = Path(path)
    if not p.parts:
        return None
    head = p.parts[0]
    if head in active or head in placeholders:
        return head
    return None


def is_workflow_trace_file(path: str, trace_dept: str, trace_rex: re.Pattern[str]) -> bool:
    p = Path(path)
    if len(p.parts) != 2:
        return False
    if p.parts[0] != trace_dept:
        return False
    return bool(trace_rex.match(p.name))


def build_issue(code: str, message: str, fix: str, severity: str = "error") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message, "fix": fix}


def validate_trace(
    trace: dict[str, Any],
    catalog: dict[str, Any],
    statuses: set[str],
    policies: set[str],
    changed_departments: set[str],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    workflow_id = str(trace.get("workflow_id", "")).strip()
    task_id = str(trace.get("task_id", "")).strip()
    reason = str(trace.get("reason", "")).strip()
    steps = trace.get("steps", [])

    if not workflow_id:
        issues.append(build_issue("WF_MISSING_ID", "workflow_id 为空", "在 Workflow Trace 中填写 workflow_id。"))
        return issues
    if workflow_id not in catalog:
        cand = ", ".join(sorted(catalog.keys())[:12])
        issues.append(
            build_issue(
                "WF_UNKNOWN_ID",
                f"workflow_id '{workflow_id}' 不在 catalog 中",
                f"改为 catalog 已定义 ID，例如：{cand}",
            )
        )
        return issues

    if not task_id:
        issues.append(build_issue("WF_MISSING_TASK", "task_id 为空", "填写稳定 task_id（如 T20260305-001）。"))
    if not reason:
        issues.append(build_issue("WF_MISSING_REASON", "reason 为空", "填写本次工作流选择理由。"))

    if not isinstance(steps, list):
        issues.append(build_issue("WF_STEPS_TYPE", "steps 不是数组", "将 steps 改为 JSON 数组。"))
        return issues

    step_map: dict[str, dict[str, Any]] = {}
    for item in steps:
        if not isinstance(item, dict):
            issues.append(build_issue("WF_STEP_OBJECT", "steps 含非对象项", "每个 steps 项必须是对象。"))
            continue
        sid = str(item.get("step_id", "")).strip()
        if not sid:
            issues.append(build_issue("WF_STEP_NO_ID", "存在 step_id 为空的步骤", "为该步骤补齐 step_id。"))
            continue
        if sid in step_map:
            issues.append(build_issue("WF_STEP_DUP", f"step_id '{sid}' 重复", "保证 step_id 在同一次 trace 内唯一。"))
            continue
        step_map[sid] = item

    wf_steps = catalog[workflow_id].get("steps", [])
    for s in wf_steps:
        sid = str(s.get("step_id", "")).strip()
        dept = str(s.get("department", "")).strip()
        policy = str(s.get("policy", "")).strip()
        allow_skip = bool(s.get("allow_skip", False))

        if policy not in policies:
            issues.append(build_issue("WF_POLICY_INVALID", f"catalog step '{sid}' policy 非法: {policy}", "修正 MD_SYNTAX_CHECK.md.workflow_enforcement.catalog。"))
            continue

        if sid not in step_map:
            issues.append(build_issue("WF_STEP_MISSING", f"缺漏步骤: {sid} ({dept})", "在 Workflow Trace.steps 中补齐该步骤。"))
            continue

        actual = step_map[sid]
        status = str(actual.get("status", "")).strip()
        evidence = actual.get("evidence", [])
        note = str(actual.get("note", "")).strip()

        if status not in statuses:
            issues.append(build_issue("WF_STATUS_INVALID", f"步骤 {sid} 的 status 非法: {status}", f"改为 {sorted(statuses)} 之一。"))
            continue

        has_evidence = isinstance(evidence, list) and len([x for x in evidence if str(x).strip()]) > 0

        if policy == "must_read":
            if status not in {"READ_ONLY", "CHANGED"}:
                issues.append(build_issue("WF_MUST_READ_STATUS", f"步骤 {sid} 必须为 READ_ONLY 或 CHANGED", "将 status 改为 READ_ONLY 或 CHANGED。"))
            if not has_evidence:
                issues.append(build_issue("WF_MUST_READ_EVIDENCE", f"步骤 {sid} 缺少 evidence", "为该步骤补充至少一条证据（文件/命令/观察）。"))

        if policy == "must_write":
            if status != "CHANGED":
                issues.append(build_issue("WF_MUST_WRITE_STATUS", f"步骤 {sid} 必须为 CHANGED", "将 status 改为 CHANGED 并完成对应部门写入。"))
            if dept not in changed_departments:
                issues.append(build_issue("WF_MUST_WRITE_DIFF", f"步骤 {sid} 标记 CHANGED 但部门 {dept} 无实际改动", f"在 {dept} 产生实际变更，或修正 workflow/步骤记录。"))

        if policy == "optional_write":
            if status == "SKIPPED_JUSTIFIED":
                if not allow_skip:
                    issues.append(build_issue("WF_SKIP_FORBIDDEN", f"步骤 {sid} 不允许 SKIPPED_JUSTIFIED", "将状态改为 READ_ONLY/CHANGED，或在规则中显式允许跳过。"))
                if not note:
                    issues.append(build_issue("WF_SKIP_NO_NOTE", f"步骤 {sid} 跳过但无 note", "补充跳过理由 note。"))

    # Extra steps are warnings (non-blocking in strict mode? keep warning)
    wf_ids = {str(s.get("step_id", "")).strip() for s in wf_steps}
    for sid in step_map:
        if sid and sid not in wf_ids:
            issues.append(build_issue("WF_EXTRA_STEP", f"存在 catalog 未定义步骤: {sid}", "删除该步骤或先在 workflow catalog 中定义。", severity="warning"))

    return issues


def render_md(report: dict[str, Any]) -> str:
    out = [
        "# Workflow Guard Report",
        "",
        f"- mode: {report['mode']}",
        f"- strict: {report['strict']}",
        f"- issues: {len(report['issues'])}",
        f"- changed_files: {len(report['changed_files'])}",
        "",
    ]
    if report.get("trace_file"):
        out.append(f"- trace_file: `{report['trace_file']}`")
        out.append("")
    if not report["issues"]:
        out.append("No workflow issues detected.")
        out.append("")
        return "\n".join(out)

    out.extend([
        "| severity | code | message | fix |",
        "| --- | --- | --- | --- |",
    ])
    for i in report["issues"]:
        out.append(f"| {i['severity']} | {i['code']} | {i['message']} | {i['fix']} |")
    out.append("")
    return "\n".join(out)


def print_issues(issues: list[dict[str, str]], fmt: str, report_only: bool) -> None:
    if fmt == "json":
        print(json.dumps({"issues": issues}, ensure_ascii=False, indent=2))
        return

    if fmt == "github":
        level = "warning" if report_only else "error"
        for i in issues:
            sev = i.get("severity", "error")
            gh_level = "warning" if (report_only or sev == "warning") else "error"
            print(f"::{gh_level} title={i['code']}::{i['message']} | fix: {i['fix']}")
        return

    # text
    for i in issues:
        print(f"[{i['severity']}] {i['code']}: {i['message']}")
        print(f"  fix: {i['fix']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="", help="department name, e.g. CHANGEMD")
    parser.add_argument("--report-only", action="store_true", help="always exit 0 and emit feedback only")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when workflow issues exist")
    parser.add_argument("--format", choices=["text", "github", "json"], default="text")
    parser.add_argument("--base-ref", default="", help="git base ref for CI diff range")
    parser.add_argument("--head-ref", default="", help="git head ref for CI diff range")
    args = parser.parse_args()

    rules = load_rules()
    wf_cfg = rules.get("workflow_enforcement", {})
    if not wf_cfg.get("enabled", False):
        report = {
            "mode": "disabled",
            "strict": bool(args.strict and not args.report_only),
            "changed_files": [],
            "issues": [],
            "trace_file": "",
        }
        REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        REPORT_MD.write_text(render_md(report), encoding="utf-8")
        print("md_workflow_guard: disabled")
        return 0

    strict_mode = bool(args.strict and not args.report_only)

    active = set(rules.get("active_departments", []))
    placeholders = set(rules.get("placeholder_departments", []))
    changed_files = git_changed_files(args.base_ref or None, args.head_ref or None)

    # Ignore self-generated reports from enforcement decision.
    changed_files_effective = [
        p
        for p in changed_files
        if p not in {REPORT_JSON.name, REPORT_MD.name}
    ]

    # Decide whether current invocation needs enforcement.
    enforce = False
    if args.scope:
        enforce = args.scope in active
    else:
        enforce = len(changed_files_effective) > 0

    report: dict[str, Any] = {
        "mode": "report-only" if args.report_only else ("strict" if strict_mode else "normal"),
        "strict": strict_mode,
        "scope": args.scope,
        "changed_files": changed_files_effective,
        "trace_file": "",
        "issues": [],
    }

    if not enforce:
        REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        REPORT_MD.write_text(render_md(report), encoding="utf-8")
        print("md_workflow_guard: no relevant changes, skipped")
        return 0

    trace_dept = str(wf_cfg.get("trace_department", "RUNMD"))
    trace_regex = re.compile(str(wf_cfg.get("trace_filename_regex", r"^RUN_INFO_WORKFLOW_[A-Z0-9_]+_\d{4}_\d{2}_\d{2}_\d{4}\.md$")))
    trace_section = str(wf_cfg.get("trace_section", "Workflow Trace"))
    statuses = set(wf_cfg.get("step_status_values", ["CHANGED", "READ_ONLY", "SKIPPED_JUSTIFIED"]))
    policies = set(wf_cfg.get("step_policy_values", ["must_read", "must_write", "optional_write"]))
    catalog = wf_cfg.get("catalog", {})

    issues: list[dict[str, str]] = []

    trace_candidates = [
        p for p in changed_files_effective if is_workflow_trace_file(p, trace_dept, trace_regex)
    ]

    if len(trace_candidates) == 0:
        issues.append(
            build_issue(
                "WF_TRACE_MISSING",
                "本次变更未发现 workflow trace 文件",
                "新增 RUN_INFO_WORKFLOW_<WORKFLOW_ID>_YYYY_MM_DD_HHMM.md 并补齐 Workflow Trace。",
            )
        )
    elif len(trace_candidates) > 1:
        issues.append(
            build_issue(
                "WF_TRACE_MULTI",
                f"检测到多个 workflow trace 文件: {trace_candidates}",
                "同一任务只保留一个主 workflow trace；多任务请拆分提交。",
            )
        )
    else:
        trace_file = trace_candidates[0]
        report["trace_file"] = trace_file
        trace_path = ROOT / trace_file
        if not trace_path.exists():
            issues.append(build_issue("WF_TRACE_NOT_FOUND", f"trace 文件不存在: {trace_file}", "确认 RUNMD 文件路径与文件名。"))
        else:
            text = trace_path.read_text(encoding="utf-8")
            sec = section_body(text, trace_section)
            if not sec:
                issues.append(
                    build_issue(
                        "WF_TRACE_SECTION_MISSING",
                        f"缺少章节 ## {trace_section}",
                        f"在 {trace_file} 增加章节 ## {trace_section} 并填入 json 轨迹。",
                    )
                )
            else:
                trace_json = parse_trace_json(sec)
                if trace_json is None:
                    issues.append(
                        build_issue(
                            "WF_TRACE_JSON_INVALID",
                            f"{trace_file} 的 Workflow Trace JSON 不可解析",
                            "使用 ```json 代码块并保证 JSON 合法。",
                        )
                    )
                else:
                    changed_depts = {
                        d
                        for d in (path_department(p, active, placeholders) for p in changed_files_effective)
                        if d in active
                    }
                    issues.extend(
                        validate_trace(
                            trace_json,
                            catalog,
                            statuses,
                            policies,
                            changed_depts,
                        )
                    )

    report["issues"] = issues
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT_MD.write_text(render_md(report), encoding="utf-8")

    if issues:
        print_issues(issues, args.format, args.report_only)
        if strict_mode:
            return 1
        return 0

    print("md_workflow_guard: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
