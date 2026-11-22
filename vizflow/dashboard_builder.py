
from pathlib import Path
import shutil


def generate_dashboard(
    df,
    plots=None,
    metadata=None,
    operations=None,
    main_variable=None,
    output_dir=None
):
    """Genera un dashboard HTML básico."""

    # --------------------------------------------------
    # Selección de variable para los KPIs
    # --------------------------------------------------

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if (
        main_variable is not None
        and main_variable in df.columns
        and main_variable in numeric_columns
    ):
        kpi_variable = main_variable
    else:
        kpi_variable = numeric_columns[0] if numeric_columns else None

    # --------------------------------------------------
    # Cálculo de KPIs
    # --------------------------------------------------

    kpis = {
        "total_registros": len(df),
        "suma": None,
        "promedio": None,
        "maximo": None
    }

    if kpi_variable is not None and not df.empty:
        kpis["suma"] = df[kpi_variable].sum()
        kpis["promedio"] = df[kpi_variable].mean()
        kpis["maximo"] = df[kpi_variable].max()

    # --------------------------------------------------
    # Construcción de tarjetas KPI
    # --------------------------------------------------

    if kpi_variable is not None:
        variable_label = f"Variable analizada: {kpi_variable}"

        suma_texto = (
            f"{kpis['suma']:,.2f}"
            if kpis["suma"] is not None
            else "N/D"
        )

        promedio_texto = (
            f"{kpis['promedio']:,.2f}"
            if kpis["promedio"] is not None
            else "N/D"
        )

        maximo_texto = (
            f"{kpis['maximo']:,.2f}"
            if kpis["maximo"] is not None
            else "N/D"
        )

    else:
        variable_label = "No hay variables numéricas disponibles"
        suma_texto = "N/D"
        promedio_texto = "N/D"
        maximo_texto = "N/D"

    kpis_html = f"""
    <div class="kpis">
        <div class="kpi">
            <h3>Total de registros</h3>
            <p>{kpis["total_registros"]:,}</p>
        </div>

        <div class="kpi">
            <h3>Suma</h3>
            <p>{suma_texto}</p>
        </div>

        <div class="kpi">
            <h3>Promedio</h3>
            <p>{promedio_texto}</p>
        </div>

        <div class="kpi">
            <h3>Máximo</h3>
            <p>{maximo_texto}</p>
        </div>
    </div>

    <p class="variable-info">{variable_label}</p>
    """

    # --------------------------------------------------
    # Configuración del dashboard
    # --------------------------------------------------

    plots = plots or []
    metadata = metadata or {}
    operations = operations or []

    if output_dir is None:
        output_dir = Path("vizflow_output")
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    tabla_html = df.to_html(index=False, border=0)

    # --------------------------------------------------
    # Construcción de historial de operaciones
    # --------------------------------------------------

    operations_html = ""

    for operation in operations:
        operations_html += f"""
        <div class="operacion">
            <strong>{operation["type"]}</strong>
            <p>{operation["description"]}</p>
        </div>
        """

    if not operations_html:
        operations_html = "<p>No se registraron operaciones.</p>"

    # --------------------------------------------------
    # Construcción de visualizaciones
    # --------------------------------------------------

    plots_dir = output_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    plots_html = ""

    for i, plot in enumerate(plots, start=1):
        plot_path = Path(plot)
        destino = plots_dir / plot_path.name

        shutil.copy2(plot_path, destino)

        ruta_html = f"plots/{plot_path.name}"

        plots_html += f"""
        <div class="grafico">
            <h3>Gráfico {i}</h3>
            <img src="{ruta_html}" alt="Gráfico {i}">
        </div>
        """

    if not plots_html:
        plots_html = """
        <p>No se generaron gráficos en este análisis.</p>
        """

    # --------------------------------------------------
    # HTML y CSS del dashboard
    # --------------------------------------------------

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>VizFlow Dashboard</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                margin: 0;
                padding: 20px;
                color: #333;
            }}

            h1 {{
                color: #1e293b;
                margin-bottom: 5px;
            }}

            .contenedor {{
                max-width: 1200px;
                margin: auto;
            }}

            .tarjeta {{
                background-color: white;
                padding: 25px;
                margin-top: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            }}

            /* KPIs */

            .kpis {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-top: 20px;
            }}

            .kpi {{
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }}

            .kpi h3 {{
                color: #64748b;
                font-size: 14px;
                margin: 0 0 12px 0;
            }}

            .kpi p {{
                color: #1e293b;
                font-size: 26px;
                font-weight: bold;
                margin: 0;
                overflow-wrap: break-word;
            }}

            .variable-info {{
                color: #64748b;
                font-size: 14px;
                margin-top: 12px;
            }}

            /* Visualizaciones */

            .grafico {{
                margin-bottom: 30px;
            }}

            .grafico img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: auto;
            }}

            /* Operaciones */

            .operacion {{
                border-left: 4px solid #64748b;
                padding: 10px 15px;
                margin-bottom: 15px;
                background-color: #f8fafc;
                border-radius: 5px;
            }}

            .operacion p {{
                margin-bottom: 0;
            }}

            /* Tabla */

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                overflow-x: auto;
            }}

            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}

            th {{
                background-color: #f1f5f9;
                color: #1e293b;
            }}

            tr:nth-child(even) {{
                background-color: #f8fafc;
            }}

            /* Adaptación a pantallas pequeñas */

            @media (max-width: 600px) {{
                body {{
                    padding: 10px;
                }}

                .tarjeta {{
                    padding: 15px;
                }}

                .kpis {{
                    grid-template-columns: 1fr;
                }}

                table {{
                    display: block;
                    overflow-x: auto;
                }}
            }}
        </style>
    </head>

    <body>
        <div class="contenedor">

            <h1>VizFlow Dashboard</h1>
            <p>Resumen del análisis de datos</p>

            {kpis_html}

            <div class="tarjeta">
                <h2>Visualizaciones</h2>
                {plots_html}
            </div>

            <div class="tarjeta">
                <h2>Operaciones aplicadas</h2>
                {operations_html}
            </div>

            <div class="tarjeta">
                <h2>Resultados del análisis</h2>
                {tabla_html}
            </div>

        </div>
    </body>
    </html>
    """

    # --------------------------------------------------
    # Generación del archivo
    # --------------------------------------------------

    output_file = output_dir / "dashboard.html"

    output_file.write_text(html, encoding="utf-8")

    return output_file

