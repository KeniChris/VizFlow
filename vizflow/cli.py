#!/usr/bin/env python3
"""Interfaz de terminal para analizar un archivo .vf."""

import argparse
import json
import sys
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path


def serialize(value):
    if isinstance(value, (Decimal, Path)):
        return str(value)
    raise TypeError(type(value).__name__)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Analizador semántico de VizFlow")
    parser.add_argument("archivo", type=Path, help="Archivo fuente .vf")
    parser.add_argument("--tabla", action="store_true", help="Mostrar datasets y esquemas de tuberías")
    parser.add_argument("--ast", action="store_true", help="Mostrar AST con tipos inferidos en JSON")
    parser.add_argument("--json", action="store_true", help="Resultado completo en JSON")
    args = parser.parse_args(argv)
    try:
        from vizflow.frontend import analyze_source
    except ModuleNotFoundError as exc:
        print(f"Falta una dependencia o el parser generado: {exc}. Ejecuta bash setup.sh "
              "y, si es necesario, bash generar.sh.", file=sys.stderr)
        return 3
    try:
        path = args.archivo.resolve()
        source = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"No se pudo leer el programa: {exc}", file=sys.stderr)
        return 3
    result = analyze_source(source, path.parent)
    analysis = result.analysis
    payload = {
        "ok": result.ok, "archivo": str(path),
        "diagnosticos": [asdict(item) for item in result.diagnostics],
        "datasets": ({name: asdict(symbol) for name, symbol in analysis.symbols.datasets.items()}
                     if analysis else {}),
        "tuberias": [asdict(item) for item in analysis.pipelines] if analysis else [],
    }
    if args.ast or args.json:
        payload["ast"] = asdict(result.program) if result.program is not None else None
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=serialize))
    else:
        for diagnostic in result.diagnostics:
            print(diagnostic.render(str(args.archivo)), file=sys.stderr)
        if result.ok:
            print("Análisis semántico correcto: 0 errores.")
        else:
            print(f"Análisis rechazado: {len(result.diagnostics)} error(es).", file=sys.stderr)
        if args.tabla and analysis:
            print("\nTABLA GLOBAL DE DATASETS")
            for name, symbol in analysis.symbols.datasets.items():
                print(f"  {name}: DATASET (declarado en línea {symbol.location.line})")
                if symbol.columns is None:
                    print("    Esquema no disponible: LOAD falló.")
                else:
                    for column in symbol.columns.values():
                        nullable = " (admite vacíos)" if column.nullable else ""
                        print(f"    {column.name}: {column.datatype}{nullable}")
            print("\nENTORNOS LOCALES AL FINAL DE CADA TUBERÍA")
            for index, pipeline in enumerate(analysis.pipelines, 1):
                print(f"  Tubería {index}: {pipeline.dataset}, línea {pipeline.location.line}")
                for column in pipeline.columns.values():
                    print(f"    {column.name}: {column.datatype}")
        if args.ast and result.program is not None:
            print("\nAST ANOTADO")
            print(json.dumps(payload["ast"], ensure_ascii=False, indent=2, default=serialize))
    return 0 if result.ok else 1 if analysis is not None else 2


if __name__ == "__main__":
    sys.exit(main())
