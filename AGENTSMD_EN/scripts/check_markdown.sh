#!/usr/bin/env bash
set -euo pipefail

# Markdown syntax/lint pass only.
# Structural validation is handled by scripts/md_validate.py.

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL_FILE="$BASE_DIR/markdown_lint_failures.txt"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required but not found" >&2
  exit 1
fi

cd "$BASE_DIR"

# Pass 1: auto-fix
npx --yes markdownlint-cli2 "**/*.md" --fix >/dev/null 2>&1 || true

# Pass 2: strict check
set +e
OUTPUT=$(npx --yes markdownlint-cli2 "**/*.md" 2>&1)
STATUS=$?
set -e

if [ "$STATUS" -ne 0 ]; then
  printf "%s\n" "$OUTPUT" > "$FAIL_FILE"
  echo "markdown lint failed. See: $FAIL_FILE" >&2
  exit 1
fi

rm -f "$FAIL_FILE"
echo "markdown lint passed"
