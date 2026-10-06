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
        "ambitos": ({scope: {name: asdict(symbol) for name, symbol in symbols.items()}
                    for scope, symbols in analysis.symbols.scopes.items()}
                   if analysis else {}),
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
            print("\nTABLA DE SÍMBOLOS POR ÁMBITOS")
            print(f"{'Ámbito':<23} {'Nombre':<20} {'Tipo':<10} {'Línea':<6} "
                  f"{'Inicializado':<12} {'Usado':<5}")
            for scope, symbols in analysis.symbols.scopes.items():
                for symbol in symbols.values():
                    initialized = "sí" if symbol.initialized else "no"
                    used = "sí" if symbol.used else "no"
                    print(f"{scope:<23} {symbol.name:<20} {symbol.type_:<10} "
                          f"{symbol.line:<6} {initialized:<12} {used:<5}")
            print("\nESQUEMAS AL FINAL DE CADA TUBERÍA")
            for index, pipeline in enumerate(analysis.pipelines, 1):
                print(f"  Tubería {index}: {pipeline.dataset}")
                for column in pipeline.columns.values():
                    print(f"    {column.name}: {column.datatype}")
        if args.ast and result.program is not None:
            print("\nAST ANOTADO")
            print(json.dumps(payload["ast"], ensure_ascii=False, indent=2, default=serialize))
    return 0 if result.ok else 1 if analysis is not None else 2


if __name__ == "__main__":
    sys.exit(main())
