"""Diagnósticos semánticos demostrables desde fuentes .vf y la interfaz real."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from vizflow.frontend import analyze_source

PROJECT = Path(__file__).resolve().parents[2]
SOURCE_CASES = {
    "sem001_dataset_no_declarado.vf": ["SEM001"],
    "sem002_dataset_duplicado.vf": ["SEM002"],
    "sem003_columna_inexistente.vf": ["SEM003"],
    "sem004_tipos_incompatibles.vf": ["SEM004"],
    "sem007_sum_texto.vf": ["SEM007"],
    "sem008_division_cero.vf": ["SEM008"],
    "sem009_scatter_texto.vf": ["SEM009"],
    "sem011_csv_inexistente.vf": ["SEM011"],
    "sem012_nombres_agrupados.vf": ["SEM012"],
    # SEM014 se alcanza usando el resultado de una agregación fallida.
    "sem014_columna_no_inicializada.vf": ["SEM007", "SEM014"],
    "sem015_formato_no_csv.vf": ["SEM015"],
}


class SemanticDiagnosticTests(unittest.TestCase):
    def test_diagnosticos_exactos_desde_archivos_vf(self):
        for name, expected in SOURCE_CASES.items():
            with self.subTest(file=name):
                path = PROJECT / "tests/test_semantico/invalidos" / name
                result = analyze_source(path.read_text(encoding="utf-8"), path.parent)
                self.assertIsNotNone(result.analysis, "Debe superar léxico y sintaxis.")
                self.assertFalse(result.ok)
                self.assertEqual([d.code for d in result.diagnostics], expected)
                self.assertTrue(all(d.phase == "semántico" for d in result.diagnostics))
                self.assertTrue(all(d.location.line > 0 and d.location.column > 0
                                    for d in result.diagnostics))

    def test_diagnosticos_exactos_desde_main_con_archivos_vf(self):
        for name, expected in SOURCE_CASES.items():
            with self.subTest(file=name):
                path = PROJECT / "tests/test_semantico/invalidos" / name
                process = subprocess.run(
                    [sys.executable, str(PROJECT / "main.py"), "--semantico", "--json", str(path)],
                    cwd=PROJECT, capture_output=True, text=True, encoding="utf-8",
                    env=dict(os.environ, PYTHONIOENCODING="utf-8"))
                self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
                payload = json.loads(process.stdout)
                self.assertFalse(payload["ok"])
                diagnostics = payload["diagnosticos"]
                self.assertEqual([d["code"] for d in diagnostics], expected)
                self.assertTrue(all(d["phase"] == "semántico" for d in diagnostics))
                self.assertTrue(all(d["location"]["line"] > 0 and d["location"]["column"] > 0
                                    for d in diagnostics))

    def test_restricciones_gramaticales_se_reportan_como_sintaxis(self):
        cases = [
            "ventas |> FILTER(monto);",
            "ventas |> FILTER(TRUE);",
            "ventas |> GROUP_BY(region, SUM());",
            "ventas |> GROUP_BY(region, COUNT(monto));",
            "ventas |> GROUP_BY(region, SUM(1));",
            "ventas |> GROUP_BY(region, SUM(monto, cantidad));",
            "ventas |> FILTER(monto > 10) |> DASHBOARD |> FILTER(monto > 20);",
            "ventas |> TRANSFORM(total = SUM(monto));",
            "ventas |> PLOT BAR(x=region, y=COUNT());",
        ]
        for body in cases:
            with self.subTest(source=body):
                result = analyze_source('DATASET ventas = LOAD "ventas.csv";\n' + body,
                                        PROJECT / "data")
                self.assertFalse(result.ok)
                self.assertIsNone(result.analysis)
                self.assertTrue(result.diagnostics)
                self.assertTrue(all(d.code == "SYN001" and d.phase == "sintáctico"
                                    for d in result.diagnostics))


if __name__ == "__main__":
    unittest.main()
