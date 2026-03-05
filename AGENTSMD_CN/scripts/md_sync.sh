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

cd "$BASE_DIR"

./scripts/check_markdown.sh

if [[ -n "$SCOPE" ]]; then
  python3 ./scripts/md_validate.py --scope "$SCOPE"
  python3 ./scripts/md_index_sync.py --scope "$SCOPE"
  python3 ./scripts/md_validate.py --scope "$SCOPE"
else
  python3 ./scripts/md_validate.py
  python3 ./scripts/md_index_sync.py
  python3 ./scripts/md_validate.py
fi

echo "md_sync: passed"
