#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
if [[ ! -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    python3 -m venv "$PROJECT_ROOT/.venv"
fi
"$PROJECT_ROOT/.venv/bin/python" -m pip install --no-index \
    --find-links="$PROJECT_ROOT/vendor" -r "$PROJECT_ROOT/requirements.txt"
printf '%s\n' "Entorno listo. Ejecuta: bash ejecutar.sh examples/valido.vf --tabla"
