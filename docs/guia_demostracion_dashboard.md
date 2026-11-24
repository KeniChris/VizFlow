# Guía de Demostración: Pipeline y Dashboard en VizFlow

Esta guía documenta cómo funciona, cómo se ejecuta y qué resultados produce el caso de prueba existente en `tests/test_codegen/entradas/dashboard/test_dashboard.vf`, pensado para reproducir la demostración en vivo durante la presentación sin modificar el compilador.

---

## 1. El ejemplo base (`test_dashboard.vf`)

Archivo: `tests/test_codegen/entradas/dashboard/test_dashboard.vf`

```vizflow
DATASET ventas = LOAD "../../datos/ventas.csv";

ventas
    |> FILTER(monto > 100)
    |> GROUP_BY(region, SUM(monto))
    |> PLOT BAR(X = region, Y = monto)
    |> DASHBOARD;
```

### Datos de entrada (`tests/test_codegen/datos/ventas.csv`)

| region | monto | cantidad | destacado |
| :--- | ---: | ---: | :--- |
| Lima | 150 | 10 | False |
| Lima | 200 | 20 | False |
| Cusco | 80 | 5 | True |
| Cusco | 120 | 15 | False |
| Arequipa | 300 | 30 | False |

### ¿Qué hace cada operación del pipeline?

1. **`LOAD "../../datos/ventas.csv"`:** carga los 5 registros del archivo CSV en el dataset `ventas`.
2. **`FILTER(monto > 100)`:** filtra únicamente las ventas con monto mayor a 100. Se descarta el registro de `Cusco` con monto `80`, quedando 4 filas.
3. **`GROUP_BY(region, SUM(monto))`:** agrupa los 4 registros restantes por `region` (en orden alfabético) y suma la columna `monto`:
   - `Arequipa`: **300**
   - `Cusco`: **120**
   - `Lima`: **350** (`150 + 200`)
4. **`PLOT BAR(X = region, Y = monto)`:** genera un gráfico de barras con `region` en el eje X y `monto` en el eje Y, y lo guarda como imagen PNG (`grafico_bar_1.png`) sin abrir ventanas interactivas.
5. **`DASHBOARD`:** ensambla un reporte web (`dashboard.html`) que reúne los KPIs principales, el gráfico generado, el historial de operaciones aplicadas y la tabla final de datos.

---

## 2. Cómo lo procesa VizFlow y qué código Python genera

Al analizar y compilar `test_dashboard.vf`, VizFlow ejecuta dos etapas principales:

1. **Frontend (`vizflow/frontend.py`):**
   - `VizFlowLexer` y `VizFlowParser` (ANTLR 4.13.1) verifican léxico y sintaxis.
   - `SemanticVisitor` (`ASTBuilder` + `SemanticAnalyzer`) construye el AST, infiere el esquema de `ventas.csv` (`region: STRING`, `monto: NUMBER`, `cantidad: NUMBER`, `destacado: BOOLEAN`) y valida tipos, columnas y ejes del gráfico.
2. **Generación de código (`vizflow/python_builder.py`):**
   - `PythonCodeBuilder.generate(program)` recorre el AST y traduce cada operación a código Python con `pandas`, `matplotlib` y `vizflow.dashboard_builder`.

### Código Python generado

```python
import pandas as pd

ventas = pd.read_csv('../../datos/ventas.csv')
ventas = ventas[(ventas['monto'] > 100)]
ventas = ventas.groupby('region', as_index=False).agg(**{'monto': ('monto', 'sum')})
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ventas.plot(kind='bar', x='region', y='monto')
plt.tight_layout()
plt.savefig('grafico_bar_1.png')
plt.close()
from vizflow.dashboard_builder import generate_dashboard

generate_dashboard(
    ventas,
    plots=['grafico_bar_1.png'],
    operations=[
        {'type': 'LOAD', 'description': 'Cargar dataset desde ../../datos/ventas.csv'},
        {'type': 'FILTER', 'description': "Filtrar registros donde (ventas['monto'] > 100)"},
        {'type': 'GROUP_BY', 'description': 'Agrupar por region utilizando SUM'},
        {'type': 'PLOT', 'description': 'Generar gráfico de tipo BAR'}
    ],
    main_variable='monto'
)
```

---

## 3. Comandos para reproducir la demostración

### Requisitos previos
- **Python 3.10 o superior** (la sintaxis de tipos del proyecto requiere 3.10+).
- Dependencias definidas en `requirements.txt`: `antlr4-python3-runtime==4.13.1`, `pandas==2.3.3` y `matplotlib==3.10.9`.

### Paso 1: Crear el entorno virtual e instalar dependencias (solo la primera vez)

```bash
python3 -m venv .venv
source .venv/bin/activate        # En Windows (PowerShell): .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
```

### Paso 2 (opcional): Mostrar el análisis semántico y la tabla de símbolos

```bash
python3 main.py --semantico tests/test_codegen/entradas/dashboard/test_dashboard.vf --tabla
```

### Paso 3 (opcional): Imprimir el código Python generado en consola

```bash
python3 -c "from pathlib import Path; from vizflow.frontend import analyze_source; from vizflow.python_builder import PythonCodeBuilder; p = Path('tests/test_codegen/entradas/dashboard/test_dashboard.vf'); r = analyze_source(p.read_text(encoding='utf-8'), p.parent); print(PythonCodeBuilder().generate(r.program))"
```

### Paso 4: Ejecutar el caso de prueba del dashboard

```bash
python3 -m unittest tests.test_codegen.test_codegen.TestCodeGeneration.test_dashboard -v
```

*(Para ejecutar toda la suite de generación de código: `python3 -m unittest discover -s tests/test_codegen -v`.)*

### Paso 5: Abrir el dashboard HTML generado

- **macOS:**
  ```bash
  open tests/test_codegen/entradas/dashboard/vizflow_output/dashboard.html
  ```
- **Linux:**
  ```bash
  xdg-open tests/test_codegen/entradas/dashboard/vizflow_output/dashboard.html
  ```
- **Windows (CMD / PowerShell):**
  ```powershell
  start tests\test_codegen\entradas\dashboard\vizflow_output\dashboard.html
  ```

---

## 4. Archivos generados y resultados esperados

Al ejecutar `test_dashboard`, el test corre el código Python generado usando `tests/test_codegen/entradas/dashboard/` como directorio de trabajo y produce los siguientes archivos:

| Archivo generado | Descripción |
| :--- | :--- |
| `tests/test_codegen/entradas/dashboard/grafico_bar_1.png` | Imagen PNG del gráfico de barras (`region` vs. `monto`) generada con `matplotlib`. |
| `tests/test_codegen/entradas/dashboard/vizflow_output/dashboard.html` | Dashboard HTML listo para abrir en el navegador. |
| `tests/test_codegen/entradas/dashboard/vizflow_output/plots/grafico_bar_1.png` | Copia del gráfico dentro de `vizflow_output/plots/` referenciada por `dashboard.html`. |

### Contenido que muestra `dashboard.html`

1. **Tarjetas KPI** (calculadas sobre `main_variable = 'monto'`):
   - **Total de registros:** `3`
   - **Suma:** `770.00`
   - **Promedio:** `256.67`
   - **Máximo:** `350.00`
2. **Visualizaciones:** inserta el gráfico de barras `plots/grafico_bar_1.png` con las barras de Arequipa (`300`), Cusco (`120`) y Lima (`350`).
3. **Operaciones aplicadas:** muestra el historial de las 4 operaciones del pipeline (`LOAD`, `FILTER`, `GROUP_BY` y `PLOT`).
4. **Resultados del análisis:** tabla HTML con el resultado final del DataFrame:

| region | monto |
| :--- | ---: |
| Arequipa | 300 |
| Cusco | 120 |
| Lima | 350 |
