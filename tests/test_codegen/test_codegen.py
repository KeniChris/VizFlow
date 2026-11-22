import json
import subprocess
import sys
import os
import unittest
from pathlib import Path

from vizflow.frontend import analyze_source
from vizflow.python_builder import PythonCodeBuilder


ROOT = Path(__file__).resolve().parent
ENTRADAS = ROOT / "entradas"


class TestCodeGeneration(unittest.TestCase):

    def ejecutar_vizflow(self, archivo, variable="ventas"):
        source_path = ENTRADAS / archivo

        source = source_path.read_text(encoding="utf-8")

        # 1. Analizar el programa VizFlow
        frontend_result = analyze_source(source, source_path.parent)

        self.assertTrue(
            frontend_result.ok,
            msg=f"Errores en {archivo}: {frontend_result.diagnostics}"
        )

        # 2. Generar código Python
        builder = PythonCodeBuilder()
        generated_code = builder.generate(frontend_result.program)

        # 3. Ejecutar el Python generado
        generated_code += (
            f"\nprint({variable}.to_json(orient='records'))\n"
        )

        env = os.environ.copy()

        env["PYTHONPATH"] = str(ROOT.parent.parent) + os.pathsep + env.get("PYTHONPATH", "")

        result = subprocess.run(
           [sys.executable, "-c", generated_code],
            cwd=source_path.parent,
            capture_output=True,
            text=True,
            env=env
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"Error ejecutando Python generado:\n{result.stderr}"
        )

        # 4. Recuperar el resultado producido
        return json.loads(result.stdout.strip())

    def test_load(self):
        resultado = self.ejecutar_vizflow("load/test_load.vf")

        self.assertEqual(len(resultado), 5)

    def test_filter(self):
        resultado = self.ejecutar_vizflow("filter/test_filter.vf")

        self.assertEqual(len(resultado), 4)

        montos = [fila["monto"] for fila in resultado]

        self.assertEqual(montos, [150, 200, 120, 300])
        
    def test_filter_logico(self):
        resultado = self.ejecutar_vizflow(
            "filter/test_filter_logico.vf"
        )

        montos = [fila["monto"] for fila in resultado]

        self.assertEqual(montos, [200, 120, 300])
        
    def test_filter_or(self):
        resultado = self.ejecutar_vizflow(
            "filter/test_filter_or.vf"
        )
        montos = [fila["monto"] for fila in resultado]
        self.assertEqual(montos, [200, 300])    
        
    def test_filter_not(self):
        resultado = self.ejecutar_vizflow(
            "filter/test_filter_not.vf"
        )
        montos = [fila["monto"] for fila in resultado]
        self.assertEqual(montos, [80])    
        
    def test_filter_complejo(self):
        resultado = self.ejecutar_vizflow(
            "filter/test_filter_complejo.vf"
        )
        montos = [fila["monto"] for fila in resultado]
        self.assertEqual(montos, [150, 200, 80, 120, 300])
        
        
    def test_transform(self):
        resultado = self.ejecutar_vizflow("transform/test_transform.vf")

        montos_dobles = [
            fila["monto_doble"] for fila in resultado
        ]

        self.assertEqual(
            montos_dobles,
            [300, 400, 160, 240, 600]
        )

    def test_groupby(self):
        resultado = self.ejecutar_vizflow("groupby/test_groupby.vf")

        esperado = [
            {"region": "Arequipa", "monto": 300},
            {"region": "Cusco", "monto": 200},
            {"region": "Lima", "monto": 350},
        ]

        self.assertEqual(resultado, esperado)
        
    def test_groupby_avg(self):
        resultado = self.ejecutar_vizflow(
            "groupby/test_groupby_avg.vf"
        )
        esperado = [
            {"region": "Arequipa", "monto": 300.0},
            {"region": "Cusco", "monto": 100.0},
            {"region": "Lima", "monto": 175.0},
        ]
        self.assertEqual(resultado, esperado)

    def test_groupby_min(self):
        resultado = self.ejecutar_vizflow(
            "groupby/test_groupby_min.vf"
        )
        esperado = [
            {"region": "Arequipa", "monto": 300},
            {"region": "Cusco", "monto": 80},
            {"region": "Lima", "monto": 150},
        ]
        self.assertEqual(resultado, esperado)

    def test_groupby_max(self):
        resultado = self.ejecutar_vizflow(
            "groupby/test_groupby_max.vf"
        )
        esperado = [
            {"region": "Arequipa", "monto": 300},
            {"region": "Cusco", "monto": 120},
            {"region": "Lima", "monto": 200},
        ]
        self.assertEqual(resultado, esperado)

    def test_groupby_count(self):
        resultado = self.ejecutar_vizflow(
            "groupby/test_groupby_count.vf"
        )
        esperado = [
            {"region": "Arequipa", "total_ventas": 1},
            {"region": "Cusco", "total_ventas": 2},
            {"region": "Lima", "total_ventas": 2},
        ]
        self.assertEqual(resultado, esperado)
        
    def test_plot_bar(self):
        archivo = ENTRADAS / "plot/test_plot_bar.vf"
        grafico = archivo.parent / "grafico_bar_1.png"

        # Evitar que un gráfico anterior falsee la prueba
        if grafico.exists():
            grafico.unlink()

        resultado = self.ejecutar_vizflow(
            "plot/test_plot_bar.vf"
        )

        self.assertEqual(len(resultado), 5)

        self.assertTrue(
            grafico.exists(),
            msg="No se generó el archivo grafico_bar_1.png"
        )

        self.assertGreater(
            grafico.stat().st_size,
            0,
            msg="El gráfico generado está vacío"
        )

    def test_plot_line(self):
        archivo = ENTRADAS / "plot/test_plot_line.vf"
        grafico = archivo.parent / "grafico_line_1.png"

        # Evitar que un gráfico anterior falsee la prueba
        if grafico.exists():
            grafico.unlink()

        resultado = self.ejecutar_vizflow(
            "plot/test_plot_line.vf"
        )

        self.assertEqual(len(resultado), 5)

        self.assertTrue(
            grafico.exists(),
            msg="No se generó el archivo grafico_line_1.png"
        )

        self.assertGreater(
            grafico.stat().st_size,
            0,
            msg="El gráfico generado está vacío"
        )
        
    def test_plot_scatter(self):
        archivo = ENTRADAS / "plot/test_plot_scatter.vf"
        grafico = archivo.parent / "grafico_scatter_1.png"

        # Evitar que un gráfico anterior falsee la prueba
        if grafico.exists():
            grafico.unlink()

        resultado = self.ejecutar_vizflow(
            "plot/test_plot_scatter.vf"
        )

        self.assertEqual(len(resultado), 5)

        self.assertTrue(
            grafico.exists(),
            msg="No se generó el archivo grafico_scatter_1.png"
        )

        self.assertGreater(
            grafico.stat().st_size,
            0,
            msg="El gráfico generado está vacío"
        )    
     
    def test_transform_complejo(self):
        resultado = self.ejecutar_vizflow(
            "transform/test_transform_complejo.vf"
        )

        promedios = [
            fila["promedio"] for fila in resultado
        ]

        self.assertEqual(
            promedios,
            [80, 110, 42.5, 67.5, 165]
        )
        
    def test_transform_resta(self):
        resultado = self.ejecutar_vizflow(
            "transform/test_transform_resta.vf"
        )

        diferencias = [
            fila["diferencia"] for fila in resultado
        ]

        self.assertEqual(
            diferencias,
            [140, 180, 75, 105, 270]
        )
        
    def test_dashboard(self):
        resultado = self.ejecutar_vizflow(
            "dashboard/test_dashboard.vf"
        )

        regiones = [
            fila["region"] for fila in resultado
        ]

        montos = [
            fila["monto"] for fila in resultado
        ]

        self.assertEqual(
            regiones,
            ["Arequipa", "Cusco", "Lima"]
        )

        self.assertEqual(
            montos,
            [300, 120, 350]
        )

    def test_pipeline(self):
        resultado = self.ejecutar_vizflow("pipeline/test_pipeline.vf")

        montos_dobles = [
            fila["monto_doble"] for fila in resultado
        ]

        self.assertEqual(
            montos_dobles,
            [300, 400, 240, 600]
        )

    def test_pipeline_completo(self):
        resultado = self.ejecutar_vizflow(
            "pipeline/test_pipeline_completo.vf"
        )

        esperado = [
            {"region": "Arequipa", "monto_doble": 600},
            {"region": "Cusco", "monto_doble": 240},
            {"region": "Lima", "monto_doble": 700},
        ]

        self.assertEqual(resultado, esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
