#!/usr/bin/env bash
set -euo pipefail

# Markdown syntax/lint pass only.
# Structural validation is handled by scripts/md_validate.py.

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL_FILE="$BASE_DIR/markdown_lint_failures.txt"
SCOPE=""

if [[ "${1:-}" == "--scope" ]]; then
  SCOPE="${2:-}"
  if [[ -z "$SCOPE" ]]; then
    echo "--scope requires a department name" >&2
    exit 1
  fi
  if [[ ! -d "$BASE_DIR/$SCOPE" ]]; then
    echo "unknown scope: $SCOPE" >&2
    exit 1
  fi
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required but not found" >&2
  exit 1
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

if [[ -n "$SCOPE" ]]; then
  TARGETS=("$SCOPE/*.md" "$SCOPE/**/*.md")
else
  TARGETS=("**/*.md")
fi

detect_python
if [[ -n "$SCOPE" ]]; then
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py --scope "$SCOPE" >/dev/null 2>&1 || true
else
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py >/dev/null 2>&1 || true
fi

# Pass 1: auto-fix
npx --yes markdownlint-cli2 "${TARGETS[@]}" --fix >/dev/null 2>&1 || true

# Pass 2: strict check
set +e
OUTPUT=$(npx --yes markdownlint-cli2 "${TARGETS[@]}" 2>&1)
STATUS=$?
set -e

if [ "$STATUS" -ne 0 ]; then
  printf "%s\n" "$OUTPUT" > "$FAIL_FILE"
  echo "markdown lint failed. See: $FAIL_FILE" >&2
  exit 1
fi

rm -f "$FAIL_FILE"
echo "markdown lint passed"
