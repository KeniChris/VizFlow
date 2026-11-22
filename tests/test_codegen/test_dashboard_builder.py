import unittest
import tempfile
from pathlib import Path

import pandas as pd

from vizflow.dashboard_builder import generate_dashboard


class TestDashboardBuilder(unittest.TestCase):

    def test_generar_dashboard_html(self):

        df = pd.DataFrame({
            "region": ["Lima", "Cusco"],
            "monto": [200, 120]
        })

        operations = [
            {
                "type": "LOAD",
                "description": "Cargar dataset desde ventas.csv"
            },
            {
                "type": "FILTER",
                "description": "Filtrar registros donde monto > 100"
            },
            {
                "type": "GROUP_BY",
                "description": "Agrupar por region utilizando SUM"
            },
            {
                "type": "PLOT",
                "description": "Generar gráfico de tipo BAR"
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            output_dir = temp_path / "vizflow_output"

            # Crear un gráfico de prueba.
            plot_path = temp_path / "grafico_bar_1.png"
            plot_path.write_bytes(b"imagen de prueba")

            ruta = generate_dashboard(
                df,
                plots=[str(plot_path)],
                operations=operations,
                output_dir=output_dir
            )

            # Verificar que se generó el archivo.
            self.assertTrue(ruta.exists())

            # Verificar nombre.
            self.assertEqual(ruta.name, "dashboard.html")

            # Verificar ubicación.
            self.assertEqual(ruta.parent, output_dir)

            # Verificar contenido general.
            contenido = ruta.read_text(encoding="utf-8")

            self.assertIn("VizFlow Dashboard", contenido)
            self.assertIn(
                "Resumen del análisis de datos",
                contenido
            )

            # Verificar datos de la tabla.
            self.assertIn("Lima", contenido)
            self.assertIn("Cusco", contenido)
            self.assertIn("200", contenido)
            self.assertIn("120", contenido)
            self.assertIn("<table", contenido)

            # Verificar la sección de gráficos.
            self.assertIn("Visualizaciones", contenido)
            self.assertIn("plots/grafico_bar_1.png", contenido)

            # Verificar que el gráfico se haya copiado.
            grafico_copiado = (
                output_dir / "plots" / "grafico_bar_1.png"
            )

            self.assertTrue(grafico_copiado.exists())

            # Verificar la sección de operaciones.
            self.assertIn("Operaciones aplicadas", contenido)

            self.assertIn("LOAD", contenido)
            self.assertIn(
                "Cargar dataset desde ventas.csv",
                contenido
            )

            self.assertIn("FILTER", contenido)
            self.assertIn(
                "Filtrar registros donde monto > 100",
                contenido
            )

            self.assertIn("GROUP_BY", contenido)
            self.assertIn(
                "Agrupar por region utilizando SUM",
                contenido
            )

            self.assertIn("PLOT", contenido)
            self.assertIn(
                "Generar gráfico de tipo BAR",
                contenido
            )


if __name__ == "__main__":
    unittest.main()
