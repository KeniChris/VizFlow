"""Integración desde texto fuente con las gramáticas reales del equipo."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from typing import TypeVar, cast

from vizflow import ast_nodes as ast
from vizflow.frontend import analyze_source
from vizflow.semantic import AnalysisResult

PROJECT = Path(__file__).resolve().parents[2]
NodeT = TypeVar("NodeT", bound=ast.Node)


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for path in (PROJECT / "data").glob("*.csv"):
            shutil.copy2(path, self.root / path.name)
        self.prefix = 'DATASET ventas = LOAD "ventas.csv";\n\n'

    def tearDown(self):
        self.temp.cleanup()

    def analyze(self, body, prefix=True):
        return analyze_source((self.prefix if prefix else "") + body, self.root)

    def valid(self, body, prefix=True) -> AnalysisResult:
        result = self.analyze(body, prefix)
        self.assertTrue(result.ok, [d.message for d in result.diagnostics])
        self.assertIsNotNone(result.analysis)
        assert result.analysis is not None
        return result.analysis

    def semantic_error(self, body, code, prefix=True) -> AnalysisResult:
        result = self.analyze(body, prefix)
        self.assertIsNotNone(result.analysis, "Debe superar léxico y sintaxis.")
        self.assertIn(code, [d.code for d in result.diagnostics])
        self.assertTrue(all(d.phase == "semántico" for d in result.diagnostics))
        assert result.analysis is not None
        return result.analysis

    def node(self, value: ast.Node, expected: type[NodeT]) -> NodeT:
        # assertIsInstance valida en ejecución; cast comunica ese tipo al editor.
        self.assertIsInstance(value, expected)
        return cast(NodeT, value)

    def pipeline(self, result: AnalysisResult) -> ast.Pipeline:
        return self.node(result.program.statements[1], ast.Pipeline)

    def condition(self, result: AnalysisResult) -> ast.Node:
        return self.node(self.pipeline(result).operations[0], ast.Filter).condition

    def expression(self, result: AnalysisResult) -> ast.Node:
        return self.node(self.pipeline(result).operations[0], ast.Transform).expression

    def syntax_error(self, body, prefix=True):
        result = self.analyze(body, prefix)
        self.assertIsNone(result.analysis)
        self.assertTrue(result.diagnostics)
        self.assertTrue(all(d.code == "SYN001" for d in result.diagnostics))
        return result

    def test_pipeline_del_informe(self):
        result = self.valid("ventas |> FILTER(monto > 500) "
                            "|> GROUP_BY(categoria, SUM(monto)) "
                            "|> PLOT BAR(x=categoria, y=monto) |> DASHBOARD;")
        self.assertEqual(set(result.pipelines[0].columns), {"categoria", "monto"})
        self.assertIsInstance(self.pipeline(result).operations[-1], ast.Dashboard)

    def test_ejemplos_de_construcciones_actualizadas(self):
        declarations = "\n".join([
            'DATASET ventas = LOAD "ventas.csv";',
            'DATASET clientes = LOAD "clientes_2026.csv";',
            'DATASET notas = LOAD "evaluaciones.csv";',
            'DATASET inventario = LOAD "stock_almacen.csv";',
            'DATASET llamadas = LOAD "call_center_log.csv";',
            'DATASET productos = LOAD "productos.csv";',
            'DATASET alumnos = LOAD "alumnos.csv";',
        ])
        examples = [
            "ventas |> FILTER(monto > 500);",
            "clientes |> FILTER(edad >= 18 AND activo == TRUE);",
            "notas |> FILTER(promedio < 11 OR asistencia < 70);",
            "inventario |> FILTER(NOT disponible == TRUE);",
            "productos |> FILTER((precio >= 100 AND stock > 0) OR destacado == TRUE);",
            "ventas |> TRANSFORM(monto_igv = monto * 1.18);",
            "clientes |> TRANSFORM(edad_meses = edad * 12);",
            "notas |> TRANSFORM(promedio = (examen1 + examen2) / 2);",
            "inventario |> TRANSFORM(valor_total = precio * cantidad + envio);",
            "ventas |> TRANSFORM(ganancia_neta = (precio_venta - costo_base) * cantidad);",
            "ventas |> GROUP_BY(categoria, SUM(monto));",
            "ventas |> GROUP_BY(region, AVG(monto));",
            "productos |> GROUP_BY(categoria, MIN(precio));",
            "productos |> GROUP_BY(categoria, MAX(precio));",
            "clientes |> GROUP_BY(region, COUNT());",
            "ventas |> PLOT BAR(x=categoria, y=monto);",
            "ventas |> PLOT LINE(x=mes, y=monto);",
            # El informe omite el ';': aquí se prueba la versión corregida.
            "clientes |> PLOT BAR(x=region, y=total_clientes);",
            "productos |> PLOT SCATTER(x=precio, y=ventas);",
            "alumnos |> PLOT BAR(x=curso, y=promedio);",
        ]
        sources = declarations.splitlines()[:5] + [declarations + "\n" + s for s in examples]
        for source in sources:
            with self.subTest(source=source):
                result = analyze_source(source, self.root)
                self.assertTrue(result.ok, [d.message for d in result.diagnostics])

    def test_punto_coma_omitido_en_ejemplo_plot_del_informe(self):
        self.syntax_error("ventas |> PLOT BAR(x=region, y=monto)")

    def test_not_se_aplica_a_comparacion_del_informe(self):
        result = self.valid("ventas |> FILTER(NOT activo == TRUE);")
        condition = self.node(self.condition(result), ast.Unary)
        self.assertIsInstance(condition.operand, ast.Binary)
        self.assertEqual(condition.inferred_type, "BOOLEAN")

    def test_precedencia_not_and_or_y_minusculas(self):
        result = self.valid('ventas |> FILTER(not activo == true and monto > 10 '
                            'or region == "Lima");')
        condition = self.node(self.condition(result), ast.Binary)
        self.assertEqual(condition.operator, "OR")
        left = self.node(condition.left, ast.Binary)
        self.assertEqual(left.operator, "AND")
        self.assertEqual(self.node(left.left, ast.Unary).operator, "NOT")
        self.assertEqual(condition.inferred_type, "BOOLEAN")

    def test_parentesis_logicos(self):
        self.valid('ventas |> FILTER((monto > 500 OR region == "Lima") AND activo != false);')

    def test_precedencia_aritmetica_y_tipo_sintetizado(self):
        result = self.valid("ventas |> TRANSFORM(total = monto + precio * cantidad);")
        expression = self.node(self.expression(result), ast.Binary)
        self.assertEqual(expression.operator, "+")
        self.assertEqual(self.node(expression.right, ast.Binary).operator, "*")
        self.assertEqual(expression.inferred_type, "NUMBER")

    def test_asociatividad_aritmetica_izquierda(self):
        result = self.valid("ventas |> TRANSFORM(total = monto - precio - cantidad);")
        expression = self.node(self.expression(result), ast.Binary)
        self.assertEqual(self.node(expression.left, ast.Binary).operator, "-")
        self.assertEqual(self.node(expression.right, ast.Column).name, "cantidad")

    def test_decimales_del_lexer_real(self):
        self.valid("ventas |> TRANSFORM(total = monto * .75 + 1. + 1e3);")

    def test_transform_visible_en_la_misma_tuberia(self):
        self.valid("ventas |> TRANSFORM(total = precio * cantidad) |> FILTER(total > 10) "
                   "|> PLOT BAR(x=categoria, y=total);")

    def test_transform_no_modifica_dataset_global(self):
        result = self.semantic_error("ventas |> TRANSFORM(total = precio * cantidad);\n"
                                     "ventas |> FILTER(total > 10);", "SEM003")
        dataset = result.symbols.datasets["ventas"]
        assert dataset.columns is not None
        self.assertNotIn("total", dataset.columns)
        self.assertIn("total", result.pipelines[0].columns)

    def test_transform_reemplaza_columna_existente(self):
        self.valid("ventas |> TRANSFORM(monto = precio * cantidad) |> FILTER(monto > 10);")

    def test_count_crea_total_del_dataset(self):
        source = 'DATASET clientes = LOAD "clientes.csv";\n' \
                 'clientes |> GROUP_BY(region, COUNT()) ' \
                 '|> PLOT BAR(x=region, y=total_clientes);'
        result = self.valid(source, prefix=False)
        schema = result.pipelines[0].columns
        self.assertEqual(set(schema), {"region", "total_clientes"})
        self.assertEqual(schema["total_clientes"].datatype, "NUMBER")

    def test_count_nombre_para_otro_dataset(self):
        result = self.valid("ventas |> GROUP_BY(region, COUNT()) "
                            "|> PLOT BAR(x=region, y=total_ventas);")
        self.assertIn("total_ventas", result.pipelines[0].columns)

    def test_pipelines_con_dashboard_opcional(self):
        self.valid("ventas |> FILTER(monto > 10);\n"
                   "ventas |> FILTER(monto > 20) |> DASHBOARD;")

    def test_ejes_mayusculas_y_varios_graficos(self):
        self.valid("ventas |> PLOT LINE(X=mes, Y=monto) "
                   "|> PLOT SCATTER(x=precio, y=cantidad) |> DASHBOARD;")

    def test_plot_conserva_esquema_para_operacion_posterior(self):
        self.valid("ventas |> PLOT BAR(x=categoria, y=monto) |> FILTER(monto > 10);")

    def test_sem001_dataset_no_declarado(self):
        self.semantic_error("fantasma |> FILTER(monto > 10);", "SEM001", prefix=False)

    def test_sem001_uso_anterior_a_declaracion(self):
        self.semantic_error('ventas |> FILTER(monto > 10);\n'
                            'DATASET ventas = LOAD "ventas.csv";', "SEM001", prefix=False)

    def test_sem002_dataset_duplicado(self):
        self.semantic_error('DATASET ventas = LOAD "ventas.csv";', "SEM002")

    def test_sem003_columna_inexistente_y_ubicacion(self):
        result = self.semantic_error("ventas |> FILTER(descuento > 10);", "SEM003")
        error = next(d for d in result.diagnostics if d.code == "SEM003")
        self.assertEqual((error.location.line, error.location.column), (3, 18))
        self.assertEqual(len(result.diagnostics), 1)

    def test_sem003_columna_derecha_de_comparacion(self):
        self.semantic_error("ventas |> FILTER(monto > inexistente);", "SEM003")

    def test_sem003_columna_descartada_por_group_by(self):
        self.semantic_error("ventas |> GROUP_BY(region, SUM(monto)) "
                            "|> PLOT BAR(x=categoria, y=monto);", "SEM003")

    def test_sem003_clave_group_by_inexistente(self):
        self.semantic_error("ventas |> GROUP_BY(inexistente, SUM(monto));", "SEM003")

    def test_sem004_aritmetica_con_texto(self):
        self.semantic_error("ventas |> TRANSFORM(total = monto + categoria);", "SEM004")

    def test_sem004_comparacion_de_tipos_diferentes(self):
        self.semantic_error('ventas |> FILTER(monto > "mucho");', "SEM004")

    def test_sem004_comparacion_ordenada_de_booleanos(self):
        self.semantic_error("ventas |> FILTER(activo > TRUE);", "SEM004")

    def test_sem007_agregaciones_numericas_sobre_texto(self):
        for name in ("SUM", "AVG", "MIN", "MAX"):
            with self.subTest(name=name):
                self.semantic_error(f"ventas |> GROUP_BY(region, {name}(categoria));", "SEM007")

    def test_sem008_division_por_cero_literal(self):
        self.semantic_error("ventas |> TRANSFORM(total = monto / 0);", "SEM008")

    def test_sem008_division_por_cero_calculable(self):
        for denominator in ("(2 - 2)", "(2 * 0)", "((4 / 2) - 2)", "(.5 - .5)"):
            with self.subTest(denominator=denominator):
                self.semantic_error(f"ventas |> TRANSFORM(total = monto / {denominator});", "SEM008")

    def test_constantes_redondeadas_no_crean_falso_cero(self):
        self.valid("ventas |> TRANSFORM(total = monto / (1e100 + 1 - 1e100));")

    def test_division_por_columna_solo_se_verifica_por_tipo(self):
        self.valid("ventas |> TRANSFORM(total = monto / cantidad);")

    def test_sem009_scatter_con_x_de_texto(self):
        self.semantic_error("ventas |> PLOT SCATTER(x=categoria, y=monto);", "SEM009")

    def test_sem009_y_de_texto(self):
        self.semantic_error("ventas |> PLOT BAR(x=region, y=categoria);", "SEM009")

    def test_sem009_line_con_x_booleano(self):
        self.semantic_error("ventas |> PLOT LINE(x=activo, y=monto);", "SEM009")

    def test_sem011_csv_inexistente_sin_cascada(self):
        result = self.semantic_error('DATASET ventas = LOAD "no_existe.csv";\n'
                                     'ventas |> FILTER(monto > 10);', "SEM011", prefix=False)
        self.assertEqual(len(result.diagnostics), 1)

    def test_sem011_encabezados_repetidos(self):
        (self.root / "ventas.csv").write_text("monto,monto\n1,2\n", encoding="utf-8")
        self.semantic_error("ventas |> FILTER(monto > 10);", "SEM011")

    def test_sem011_csv_con_fila_incompleta(self):
        (self.root / "ventas.csv").write_text("monto,region\n1\n", encoding="utf-8")
        self.semantic_error("ventas |> FILTER(monto > 10);", "SEM011")

    def test_sem011_csv_vacio(self):
        (self.root / "ventas.csv").write_text("", encoding="utf-8")
        self.semantic_error("ventas |> FILTER(monto > 10);", "SEM011")

    def test_sem012_colision_de_clave_y_resultado_agregado(self):
        self.semantic_error("ventas |> GROUP_BY(monto, SUM(monto));", "SEM012")

    def test_null_igualdad_y_desigualdad(self):
        self.valid("ventas |> FILTER(monto == NULL);\nventas |> FILTER(categoria != null);")

    def test_null_columna_sin_muestras_de_tipo(self):
        (self.root / "ventas.csv").write_text("monto,region\n,Lima\n", encoding="utf-8")
        result = self.valid("ventas |> FILTER(monto == NULL);")
        condition = self.node(self.condition(result), ast.Binary)
        self.assertEqual(condition.left.inferred_type, "UNKNOWN")
        self.assertEqual(condition.right.inferred_type, "NULL")
        self.assertEqual(condition.inferred_type, "BOOLEAN")

    def test_null_no_admite_comparacion_ordenada(self):
        self.semantic_error("ventas |> FILTER(monto > NULL);", "SEM004")

    def test_sem004_columna_sin_muestras_en_comparacion_numerica(self):
        (self.root / "ventas.csv").write_text("monto,region\n,Lima\n", encoding="utf-8")
        self.semantic_error("ventas |> FILTER(monto > 10);", "SEM004")

    def test_csv_bom_vacios_y_decimales(self):
        (self.root / "ventas.csv").write_text("\ufeffmonto,activo\n1.5,true\n,false\n", encoding="utf-8")
        result = self.valid("ventas |> FILTER(monto >= 1.5 AND activo == TRUE);")
        dataset = result.symbols.datasets["ventas"]
        assert dataset.columns is not None
        column = dataset.columns["monto"]
        self.assertTrue(column.nullable)
        self.assertEqual(column.datatype, "NUMBER")

    def test_csv_tipo_mixto_se_considera_texto(self):
        (self.root / "ventas.csv").write_text("monto,region\n1,Lima\ntexto,Lima\n", encoding="utf-8")
        self.semantic_error("ventas |> GROUP_BY(region, SUM(monto));", "SEM007")

    def test_cadenas_escapadas_del_lexer_real(self):
        result = self.valid(r'ventas |> FILTER(categoria == "A\"B\\C\q");')
        condition = self.node(self.condition(result), ast.Binary)
        self.assertEqual(self.node(condition.right, ast.Literal).value, 'A"B\\C\\q')

    def test_error_char_es_error_lexico(self):
        body = "ventas |> FILTER(monto @ 10);"
        result = self.analyze(body)
        self.assertIsNone(result.analysis)
        self.assertEqual([d.code for d in result.diagnostics], ["LEX001"])
        self.assertEqual(result.diagnostics[0].location.column, body.index("@") + 1)

    def test_sintaxis_actual_rechaza_count_con_argumento(self):
        self.syntax_error("ventas |> GROUP_BY(region, COUNT(monto));")

    def test_sintaxis_actual_rechaza_sum_sin_argumento(self):
        self.syntax_error("ventas |> GROUP_BY(region, SUM());")

    def test_sintaxis_actual_rechaza_agregacion_en_plot(self):
        self.syntax_error("ventas |> PLOT BAR(x=region, y=COUNT());")

    def test_sintaxis_actual_rechaza_filtro_sin_comparacion(self):
        self.syntax_error("ventas |> FILTER(monto + 10);")

    def test_sintaxis_actual_rechaza_dashboard_intermedio(self):
        self.syntax_error("ventas |> FILTER(monto > 10) |> DASHBOARD |> FILTER(monto > 20);")

    def test_sintaxis_actual_rechaza_programa_vacio(self):
        self.syntax_error("", prefix=False)

    def test_archivos_sintacticos_del_equipo_conservan_su_fase(self):
        for path in sorted((PROJECT / "tests/test_sintactico/validos").glob("*.vf")):
            with self.subTest(path=path.name):
                result = analyze_source(path.read_text(encoding="utf-8"), self.root)
                self.assertIsNotNone(result.analysis)
        for path in sorted((PROJECT / "tests/test_sintactico/invalidos").glob("*.vf")):
            with self.subTest(path=path.name):
                result = analyze_source(path.read_text(encoding="utf-8"), self.root)
                self.assertIsNone(result.analysis)
                self.assertTrue(all(d.code == "SYN001" for d in result.diagnostics))

    def test_ejemplos_validos_incluidos_en_paquete(self):
        for path in sorted((PROJECT / "examples").glob("*.vf")):
            with self.subTest(path=path.name):
                result = analyze_source(path.read_text(encoding="utf-8"), path.parent)
                self.assertTrue(result.ok, [d.message for d in result.diagnostics])


class DriverTests(unittest.TestCase):
    def execute(self, *arguments: str, cwd: str | Path = PROJECT):
        return subprocess.run([sys.executable, str(PROJECT / "main.py"), *arguments],
                              cwd=cwd, capture_output=True, text=True,
                              encoding="utf-8",
                              env=dict(os.environ, PYTHONIOENCODING="utf-8"))

    def test_driver_legacy_sigue_funcionando(self):
        result = self.execute("tests/test_sintactico/validos/test_06_pipeline_valido2.vf")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Análisis sintáctico completado sin errores", result.stdout)
        self.assertNotIn("SEM011", result.stdout + result.stderr)

    def test_driver_semantico_json_y_count(self):
        result = self.execute("--semantico", "examples/count.vf", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["ok"])
        self.assertIn("total_clientes", data["tuberias"][0]["columns"])

    def test_driver_ast_con_null_serializable(self):
        result = self.execute("--semantico", "examples/null.vf", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        expression = json.loads(result.stdout)["ast"]["statements"][1]["operations"][0]["condition"]
        self.assertIsNone(expression["right"]["value"])

    def test_driver_exit_uno_semantico(self):
        result = self.execute("examples/errores/sem007_sum_texto.vf", "--semantico")
        self.assertEqual(result.returncode, 1)
        self.assertIn("SEM007", result.stderr)

    def test_driver_exit_dos_sintactico(self):
        result = self.execute("--semantico", "examples/errores/sintactico.vf")
        self.assertEqual(result.returncode, 2)
        self.assertIn("SYN001", result.stderr)

    def test_driver_exit_dos_lexico(self):
        result = self.execute("--semantico", "examples/errores/lexico.vf")
        self.assertEqual(result.returncode, 2)
        self.assertIn("LEX001", result.stderr)
        self.assertNotIn("SYN001", result.stderr)

    def test_driver_exit_tres_fuente_inexistente(self):
        result = self.execute("--semantico", "fuente_que_no_existe.vf")
        self.assertEqual(result.returncode, 3)

    def test_csv_relativo_al_fuente_desde_otro_directorio(self):
        with tempfile.TemporaryDirectory() as other:
            result = self.execute("--semantico", str(PROJECT / "examples/valido.vf"), cwd=other)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
