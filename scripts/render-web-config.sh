#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${1:-${API_BASE_URL:-http://localhost:8000/api/v1}}"
TARGET="${2:-apps/web/runtime-config.js}"

cat > "${TARGET}" <<EOF
window.BEACON_CONFIG = {
  API_BASE_URL: "${API_BASE_URL}",
};
EOF

printf 'Wrote %s with API_BASE_URL=%s\n' "${TARGET}" "${API_BASE_URL}"
