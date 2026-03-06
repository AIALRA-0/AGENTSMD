#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_FILE="tests/integration/configValidationFlow.test.js"
RUN_FLAG="${AGENTSMD_RUN_CONFIG_VALIDATION_FLOW:-0}"
FAIL_ON_SKIP="${AGENTSMD_FAIL_ON_SKIP:-0}"

cd "$BASE_DIR"

if [[ "$RUN_FLAG" != "1" ]]; then
  echo "integration test skipped: AGENTSMD_RUN_CONFIG_VALIDATION_FLOW!=1"
  exit 0
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required for integration test" >&2
  exit 1
fi

if [[ ! -f "$TEST_FILE" ]]; then
  echo "integration test file not found: $TEST_FILE"
  if [[ "$FAIL_ON_SKIP" == "1" ]]; then
    echo "AGENTSMD_FAIL_ON_SKIP=1, failing on missing integration test file" >&2
    exit 1
  fi
  exit 0
fi

if command -v python3 >/dev/null 2>&1; then
  set +e
  python3 - <<'PY'
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    s.close()
except OSError:
    raise SystemExit(1)
raise SystemExit(0)
PY
  PORT_OK=$?
  set -e
  if [[ "$PORT_OK" -ne 0 ]]; then
    echo "integration test skipped: current environment does not allow local port listen"
    if [[ "$FAIL_ON_SKIP" == "1" ]]; then
      echo "AGENTSMD_FAIL_ON_SKIP=1, failing because port-listen is unavailable" >&2
      exit 1
    fi
    exit 0
  fi
fi

echo "running integration test: $TEST_FILE"
node --test "$TEST_FILE"
