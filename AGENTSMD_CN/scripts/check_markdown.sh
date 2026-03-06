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

detect_markdownlint() {
  local local_bin="$BASE_DIR/node_modules/.bin/markdownlint-cli2"
  if [[ -x "$local_bin" ]]; then
    MD_LINT=("$local_bin")
    return
  fi

  if command -v markdownlint-cli2 >/dev/null 2>&1; then
    MD_LINT=("markdownlint-cli2")
    return
  fi

  if command -v npx >/dev/null 2>&1 && npx --no-install markdownlint-cli2 --version >/dev/null 2>&1; then
    MD_LINT=("npx" "--no-install" "markdownlint-cli2")
    return
  fi

  cat >&2 <<'EOF'
markdownlint-cli2 not found.
Install local dependency first (offline-safe after first install):
  npm install --no-audit --no-fund
EOF
  exit 1
}

cd "$BASE_DIR"

if [[ -n "$SCOPE" ]]; then
  TARGETS=("$SCOPE/*.md" "$SCOPE/**/*.md")
else
  TARGETS=("**/*.md")
fi

detect_python
detect_markdownlint
if [[ -n "$SCOPE" ]]; then
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py --scope "$SCOPE" >/dev/null 2>&1 || true
else
  "${PY_CMD[@]}" ./scripts/normalize_blank_lines.py >/dev/null 2>&1 || true
fi

IGNORE_ARGS=(
  "--ignore" "node_modules/**"
  "--ignore" ".venv*/**"
  "--ignore" "agentsmd_web/node_modules/**"
)

# Pass 1: auto-fix
"${MD_LINT[@]}" "${TARGETS[@]}" "${IGNORE_ARGS[@]}" --fix >/dev/null 2>&1 || true

# Pass 2: strict check
set +e
OUTPUT=$("${MD_LINT[@]}" "${TARGETS[@]}" "${IGNORE_ARGS[@]}" 2>&1)
STATUS=$?
set -e

if [ "$STATUS" -ne 0 ]; then
  printf "%s\n" "$OUTPUT" > "$FAIL_FILE"
  echo "markdown lint failed. See: $FAIL_FILE" >&2
  exit 1
fi

rm -f "$FAIL_FILE"
echo "markdown lint passed"
