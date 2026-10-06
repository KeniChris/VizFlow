#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_ROOT"
"$PROJECT_ROOT/.venv/bin/python" run_tests.py
