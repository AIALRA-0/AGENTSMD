#!/usr/bin/env bash
set -euo pipefail

# AGENTSMD sync pipeline
# How to extend:
# - Add departments/rules in AGENTS.md machine-readable block.
# - This script intentionally remains orchestration-only.

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCOPE=""

if [[ "${1:-}" == "--scope" ]]; then
  SCOPE="${2:-}"
  if [[ -z "$SCOPE" ]]; then
    echo "--scope requires a department name" >&2
    exit 1
  fi
fi

detect_python() {
  if command -v python3 >/dev/null 2>&1; then
    PY_CMD=(python3)
  elif command -v python >/dev/null 2>&1; then
    PY_CMD=(python)
  elif command -v py >/dev/null 2>&1; then
    PY_CMD=(py -3)
  else
    echo "python is required but not found (tried: python3, python, py -3)" >&2
    exit 1
  fi
}

cd "$BASE_DIR"
detect_python

if [[ -n "$SCOPE" ]]; then
  ./scripts/check_markdown.sh --scope "$SCOPE"
  "${PY_CMD[@]}" ./scripts/md_validate.py --scope "$SCOPE" --auto-fix-index
  "${PY_CMD[@]}" ./scripts/md_index_sync.py --scope "$SCOPE"
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py --scope "$SCOPE"
  ./scripts/check_markdown.sh --scope "$SCOPE"
  "${PY_CMD[@]}" ./scripts/md_validate.py --scope "$SCOPE" --auto-fix-index
  "${PY_CMD[@]}" ./scripts/md_workflow_guard.py --scope "$SCOPE" --strict
else
  ./scripts/check_markdown.sh
  "${PY_CMD[@]}" ./scripts/md_validate.py --auto-fix-index
  "${PY_CMD[@]}" ./scripts/md_index_sync.py
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py
  ./scripts/check_markdown.sh
  "${PY_CMD[@]}" ./scripts/md_validate.py --auto-fix-index
  "${PY_CMD[@]}" ./scripts/md_workflow_guard.py --strict
fi

echo "md_sync: passed"
