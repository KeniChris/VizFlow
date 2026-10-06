#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
exec "$PROJECT_ROOT/.venv/bin/python" "$PROJECT_ROOT/main.py" --semantico "$@"
