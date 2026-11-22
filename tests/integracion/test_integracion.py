"""Ejecutar desde la raíz: python3 -m unittest discover -s tests/integracion -v."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from antlr4 import CommonTokenStream, FileStream

from gen.VizFlowLexer import VizFlowLexer
from gen.VizFlowParser import VizFlowParser
from vizflow.ast_nodes import Location
from vizflow.diagnostics import Diagnostic
from vizflow.frontend import CollectErrors
from vizflow.python_builder import PythonCodeBuilder
from vizflow.semantic_visitor import SemanticVisitor


RAIZ = Path(__file__).resolve().parents[2]
CASOS = Path(__file__).resolve().parent


@contextmanager
def etapa(nombre):
    print(f"[EN CURSO] {nombre}", flush=True)
    try:
        yield
    except Exception:
        print(f"[FALLO] {nombre}", flush=True)
        raise
    else:
        print(f"[OK] {nombre}", flush=True)


class TestIntegracionVizFlow(unittest.TestCase):
    def comprobar_diagnosticos(self, archivo, diagnosticos):
        self.assertFalse(
            diagnosticos,
            "\n".join(diagnostico.render(archivo.name) for diagnostico in diagnosticos),
        )

    def test_pipeline_completo_con_dashboard(self):
        # LOAD usa una ruta relativa. Copiar ambas entradas permite ejecutar en
        # un directorio limpio donde también se guardan el gráfico y el HTML.
        with tempfile.TemporaryDirectory(prefix="vizflow-integracion-") as temporal:
            carpeta = Path(temporal)
            entrada = carpeta / "pipeline_completo.vf"
            shutil.copyfile(CASOS / entrada.name, entrada)
            shutil.copyfile(CASOS / "ventas.csv", carpeta / "ventas.csv")
            print(f"\nPrograma de integración: {entrada.name}", flush=True)

            with etapa("1/6 Análisis léxico"):
                lexer = VizFlowLexer(FileStream(str(entrada), encoding="utf-8"))
                errores_lexicos = CollectErrors("léxico", "LEX001")
                lexer.removeErrorListeners()
                lexer.addErrorListener(errores_lexicos)
                tokens = CommonTokenStream(lexer)
                tokens.fill()
                errores_lexicos.diagnostics.extend(
                    Diagnostic(
                        "LEX001",
                        f"Carácter no reconocido {token.text!r}.",
                        Location(token.line, token.column + 1),
                        "léxico",
                    )
                    for token in tokens.tokens
                    if token.type == VizFlowLexer.ERROR_CHAR
                )
                self.comprobar_diagnosticos(entrada, errores_lexicos.diagnostics)

            with etapa("2/6 Análisis sintáctico"):
                parser = VizFlowParser(tokens)
                errores_sintacticos = CollectErrors("sintáctico", "SYN001")
                parser.removeErrorListeners()
                parser.addErrorListener(errores_sintacticos)
                arbol = parser.programa()
                self.comprobar_diagnosticos(entrada, errores_sintacticos.diagnostics)

            with etapa("3/6 Análisis semántico"):
                analisis = SemanticVisitor(entrada.parent).visit(arbol)
                self.comprobar_diagnosticos(entrada, analisis.diagnostics)

            with etapa("4/6 Generación de código Python"):
                codigo = PythonCodeBuilder().generate(analisis.program)
                self.assertTrue(codigo.strip(), "El generador devolvió código vacío.")
                programa_python = carpeta / "pipeline_completo.py"
                compile(codigo, programa_python.name, "exec")
                programa_python.write_text(codigo, encoding="utf-8")
                print(f"\nCódigo Python generado:\n{codigo}", flush=True)

            with etapa("5/6 Ejecución del código Python"):
                # run_path ejecuta el archivo generado y permite leer su tabla
                # de ventas para contrastarla con los totales esperados.
                resultado_json = carpeta / "resultado.json"
                inspeccionar_resultado = (
                    "import runpy, sys\n"
                    "from pathlib import Path\n"
                    "variables = runpy.run_path(sys.argv[1], run_name='__main__')\n"
                    "ventas = variables['ventas'].to_json(orient='records')\n"
                    "Path(sys.argv[2]).write_text(ventas, encoding='utf-8')\n"
                )
                entorno = os.environ.copy()
                rutas_python = [str(RAIZ)]
                if entorno.get("PYTHONPATH"):
                    rutas_python.append(entorno["PYTHONPATH"])
                entorno["PYTHONPATH"] = os.pathsep.join(rutas_python)
                entorno["PYTHONIOENCODING"] = "utf-8"
                entorno["MPLCONFIGDIR"] = str(carpeta / "matplotlib")

                resultado = subprocess.run(
                    [sys.executable, "-c", inspeccionar_resultado, str(programa_python), str(resultado_json)],
                    cwd=carpeta,
                    env=entorno,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=30,
                )
                self.assertEqual(
                    resultado.returncode,
                    0,
                    f"Python terminó con código {resultado.returncode}.\n"
                    f"Salida: {resultado.stdout}\nErrores: {resultado.stderr}",
                )
                filas = json.loads(resultado_json.read_text(encoding="utf-8"))
                self.assertCountEqual(
                    filas,
                    [
                        {"region": "Arequipa", "monto_doble": 600},
                        {"region": "Cusco", "monto_doble": 240},
                        {"region": "Lima", "monto_doble": 700},
                    ],
                )
                print(f"Totales verificados por región: {filas}", flush=True)

            with etapa("6/6 Verificación del dashboard HTML"):
                salida = carpeta / "vizflow_output"
                dashboard = salida / "dashboard.html"
                self.assertTrue(dashboard.is_file(), "No se generó vizflow_output/dashboard.html.")
                html = dashboard.read_text(encoding="utf-8")
                self.assertIn("VizFlow Dashboard", html)
                self.assertIn("<table", html)

                grafico = Path("plots/grafico_bar_1.png")
                self.assertIn(grafico.as_posix(), html)
                self.assertTrue((salida / grafico).is_file(), "Falta el gráfico enlazado en el HTML.")
                with (salida / grafico).open("rb") as imagen:
                    self.assertEqual(imagen.read(8), b"\x89PNG\r\n\x1a\n", "El gráfico no es un PNG.")
                print("Dashboard generado en vizflow_output/dashboard.html con su gráfico.", flush=True)
