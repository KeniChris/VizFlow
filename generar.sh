#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
command -v java >/dev/null || { printf '%s\n' "Se necesita Java para regenerar ANTLR." >&2; exit 3; }
cd "$PROJECT_ROOT"
java -jar "$PROJECT_ROOT/tools/antlr-4.13.1-complete.jar" \
    -Dlanguage=Python3 -visitor -o gen VizFlowLexer.g4
java -jar "$PROJECT_ROOT/tools/antlr-4.13.1-complete.jar" \
    -Dlanguage=Python3 -visitor -lib gen -o gen VizFlowParser.g4
printf '%s\n' "Lexer, parser, listener y visitor generados con ANTLR 4.13.1."
