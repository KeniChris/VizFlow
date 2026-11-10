"""Contrato de los 15 diagnósticos con la gramática actual.

Los errores que el parser ya impide se prueban sobre el AST directamente;
una entrada rechazada como SYN001 no demuestra una validación semántica.
"""

import unittest
from decimal import Decimal
from pathlib import Path

from vizflow import ast_nodes as ast
from vizflow.frontend import analyze_source
from vizflow.semantic import SemanticAnalyzer
from vizflow.symbols import BOOLEAN, NULL, NUMBER, STRING

PROJECT = Path(__file__).resolve().parents[2]
LOCATION = ast.Location(10, 3)


class SemanticDiagnosticTests(unittest.TestCase):
    def analyze_ast(self, operations):
        program = ast.Program(LOCATION, [
            ast.LoadDataset(LOCATION, "ventas", "ventas.csv"),
            ast.Pipeline(LOCATION, "ventas", operations),
        ])
        return SemanticAnalyzer(PROJECT / "data").analyze(program)

    def assert_ast_error(self, operations, code):
        result = self.analyze_ast(operations)
        self.assertFalse(result.ok)
        self.assertEqual([d.code for d in result.diagnostics], [code])
        diagnostic = result.diagnostics[0]
        self.assertEqual(diagnostic.phase, "semántico")
        self.assertEqual(diagnostic.location, LOCATION)
        self.assertTrue(diagnostic.message)
        return result

    def test_diagnosticos_exactos_desde_archivos_vf(self):
        cases = {
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
        for name, expected in cases.items():
            with self.subTest(file=name):
                path = PROJECT / "tests/test_semantico/invalidos" / name
                result = analyze_source(path.read_text(encoding="utf-8"), path.parent)
                self.assertIsNotNone(result.analysis, "Debe superar léxico y sintaxis.")
                self.assertFalse(result.ok)
                self.assertEqual([d.code for d in result.diagnostics], expected)
                self.assertTrue(all(d.phase == "semántico" for d in result.diagnostics))
                self.assertTrue(all(d.location.line > 0 and d.location.column > 0
                                    for d in result.diagnostics))

    def test_gramatica_rechaza_las_guardas_antes_de_la_semantica(self):
        cases = [
            ("SEM005", "ventas |> FILTER(monto);"),
            ("SEM005", "ventas |> FILTER(TRUE);"),
            ("SEM006", "ventas |> GROUP_BY(region, SUM());"),
            ("SEM006", "ventas |> GROUP_BY(region, COUNT(monto));"),
            ("SEM006", "ventas |> GROUP_BY(region, SUM(1));"),
            ("SEM006", "ventas |> GROUP_BY(region, SUM(monto, cantidad));"),
            ("SEM010", "ventas |> FILTER(monto > 10) |> DASHBOARD "
                       "|> FILTER(monto > 20);"),
            ("SEM013", "ventas |> TRANSFORM(total = SUM(monto));"),
            ("SEM013", "ventas |> PLOT BAR(x=region, y=COUNT());"),
        ]
        for guard, body in cases:
            with self.subTest(guard=guard, source=body):
                result = analyze_source('DATASET ventas = LOAD "ventas.csv";\n' + body,
                                        PROJECT / "data")
                self.assertFalse(result.ok)
                self.assertIsNone(result.analysis)
                self.assertTrue(result.diagnostics)
                self.assertTrue(all(d.code == "SYN001" and d.phase == "sintáctico"
                                    for d in result.diagnostics))

    def test_sem005_filter_no_booleano_en_ast(self):
        for condition in (ast.Column(LOCATION, "monto"),
                          ast.Literal(LOCATION, "texto", STRING),
                          ast.Literal(LOCATION, None, NULL)):
            with self.subTest(condition=condition):
                self.assert_ast_error([ast.Filter(LOCATION, condition)], "SEM005")

    def test_sem006_aridad_y_argumentos_de_agregaciones_en_ast(self):
        column = ast.Column(LOCATION, "monto")
        cases = [
            ("SUM", []),
            ("AVG", []),
            ("MIN", [column, ast.Column(LOCATION, "cantidad")]),
            ("MAX", [ast.Literal(LOCATION, Decimal("1"), NUMBER)]),
            ("COUNT", [column]),
        ]
        for function, arguments in cases:
            with self.subTest(function=function, arguments=arguments):
                aggregate = ast.Aggregate(LOCATION, function, arguments)
                self.assert_ast_error([ast.GroupBy(LOCATION, "region", [aggregate])],
                                      "SEM006")

    def test_sem009_ejes_invalidos_en_ast(self):
        x = ast.Axis(LOCATION, "x", ast.Column(LOCATION, "region"))
        y = ast.Axis(LOCATION, "y", ast.Column(LOCATION, "monto"))
        cases = [
            ("desconocido", [x, y, ast.Axis(LOCATION, "z", ast.Column(LOCATION, "monto"))]),
            ("repetido", [x, x, y]),
            ("ausente", [x]),
            ("sin_columna", [ast.Axis(LOCATION, "x", ast.Literal(LOCATION, Decimal("1"), NUMBER)), y]),
        ]
        for name, axes in cases:
            with self.subTest(case=name):
                self.assert_ast_error([ast.Plot(LOCATION, "BAR", axes)], "SEM009")

    def test_sem010_operacion_despues_de_dashboard_en_ast(self):
        operations = [ast.Dashboard(LOCATION),
                      ast.Filter(LOCATION, ast.Literal(LOCATION, True, BOOLEAN))]
        self.assert_ast_error(operations, "SEM010")

    def test_sem013_agregacion_fuera_de_group_by_en_ast(self):
        for operation_type in ("TRANSFORM", "FILTER"):
            with self.subTest(operation=operation_type):
                call = ast.Aggregate(LOCATION, "SUM", [ast.Column(LOCATION, "monto")])
                operation = (ast.Transform(LOCATION, "total", call)
                             if operation_type == "TRANSFORM" else ast.Filter(LOCATION, call))
                self.assert_ast_error([operation], "SEM013")

    def test_ast_valido_no_activa_las_guardas(self):
        for function in ("SUM", "AVG", "MIN", "MAX", "COUNT"):
            with self.subTest(function=function):
                arguments = [] if function == "COUNT" else [ast.Column(LOCATION, "total")]
                operations = [
                    ast.Filter(LOCATION, ast.Literal(LOCATION, True, BOOLEAN)),
                    ast.Transform(LOCATION, "total", ast.Binary(
                        LOCATION, "*", ast.Column(LOCATION, "monto"),
                        ast.Literal(LOCATION, Decimal("2"), NUMBER))),
                    ast.GroupBy(LOCATION, "region", [ast.Aggregate(LOCATION, function, arguments)]),
                    ast.Dashboard(LOCATION),
                ]
                result = self.analyze_ast(operations)
                self.assertTrue(result.ok, result.diagnostics)


if __name__ == "__main__":
    unittest.main()
