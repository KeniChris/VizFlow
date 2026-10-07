# VizFlow - Compilador para Análisis y Visualización de Datos

## Información del Proyecto
* **Curso:** 1ACC0218 - Teoría de Compiladores (UPC)
* **Sección:** 4889
* **Docente:** José Luis Soncco Álvarez
* **Integrantes del Grupo:**
  * Pamela Rivera Contreras (U202216662)
  * Piero Antonio Aguilar Anticona (U202419995)
  * Leicy Cristell Cahuana López (U20231E777)

---

## 1. Descripción de VizFlow
**VizFlow** es un lenguaje de dominio específico (DSL) diseñado para que profesionales de áreas analíticas (Economía, Estadística, Administración, etc.) puedan realizar ingesta, limpieza, agregación y visualización de datos de manera secuencial y legible.

El lenguaje se basa en el operador de tubería (**`|>`**), permitiendo encadenar operaciones directamente sobre conjuntos de datos sin necesidad de variables intermedias.

---

## 2. Especificación del Analizador Léxico (Tokens y Lexemas)
Conforme a los requerimientos del Trabajo Parcial y la notación explicada en clase, la siguiente tabla define la especificación del léxico en formato **`Token : Lista de Lexemas / Expresión Regular`**:

| Categoría | Nombre del Token | Lexemas / Patrón (Expresión Regular) | Descripción |
| :--- | :--- | :--- | :--- |
| **Comandos Principales** | `DATASET` | `'DATASET'` | Declaración de un nuevo dataset |
| | `LOAD` | `'LOAD'` | Instrucción para cargar archivos CSV |
| | `FILTER` | `'FILTER'` | Operación de filtrado condicional |
| | `TRANSFORM` | `'TRANSFORM'` | Creación de columnas por cálculo |
| | `GROUP_BY` | `'GROUP_BY'` | Agrupamiento tabular |
| | `PLOT` | `'PLOT'` | Generación de visualizaciones |
| | `DASHBOARD` | `'DASHBOARD'` | Instrucción de renderizado y cierre |
| **Funciones Estadísticas** | `SUM` | `'SUM'` | Sumatoria acumulada |
| | `AVG` | `'AVG'` | Promedio o media aritmética |
| | `MIN` | `'MIN'` | Valor mínimo |
| | `MAX` | `'MAX'` | Valor máximo |
| | `COUNT` | `'COUNT'` | Conteo de registros o frecuencias |
| **Tipos de Gráficos** | `BAR` | `'BAR'` | Gráfico de barras |
| | `LINE` | `'LINE'` | Gráfico de líneas temporales |
| | `SCATTER` | `'SCATTER'` | Gráfico de dispersión |
| **Constantes / Lógicos** | `TRUE` | `'true'`, `'TRUE'` | Booleano verdadero |
| | `FALSE` | `'false'`, `'FALSE'` | Booleano falso |
| | `NULL` | `'null'`, `'NULL'` | Valor nulo o faltante |
| | `AND` | `'and'`, `'AND'` | Conjunción lógica textual |
| | `OR` | `'or'`, `'OR'` | Disyunción lógica textual |
| | `NOT` | `'not'`, `'NOT'` | Negación lógica textual |
| **Operador Tubería** | `PIPE` | `'\|>'` | Operador pipeline de encadenamiento |
| **Operadores Relacionales**| `EQ` | `'=='` | Igualdad |
| | `NEQ` | `'!='` | Desigualdad |
| | `LTE` | `'<='` | Menor o igual que |
| | `GTE` | `'>='` | Mayor o igual que |
| | `LT` | `'<'` | Menor que |
| | `GT` | `'>'` | Mayor que |
| **Operador Asignación** | `ASSIGN` | `'='` | Asignación en declaración o parámetros |
| **Operadores Aritméticos** | `PLUS` | `'+'` | Suma |
| | `MINUS` | `'-'` | Resta |
| | `STAR` | `'*'` | Multiplicación |
| | `SLASH` | `'/'` | División |
| | `MOD` | `'%'` | Módulo o residuo |
| **Operadores Lógicos (Ops)**| `AND_OP` | `'&&'` | Conjunción simbólica |
| | `OR_OP` | `'\|\|'` | Disyunción simbólica |
| | `NOT_OP` | `'!'` | Negación simbólica |
| **Delimitadores** | `LPAREN` | `'('` | Paréntesis izquierdo |
| | `RPAREN` | `')'` | Paréntesis derecho |
| | `COMMA` | `','` | Separador de argumentos |
| | `SEMI` | `';'` | Fin de instrucción |
| **Literales** | `STRING_LIT` | `'"' (~["\r\n\\] \| '\\' .)* '"'` | Cadenas de texto entre comillas dobles |
| | `FLOAT_LIT` | `[0-9]+ '.' [0-9]* ([eE][+-]?[0-9]+)?` | Número decimal / punto flotante |
| | `INT_LIT` | `[0-9]+` | Número entero |
| **Identificadores** | `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` | Nombres de datasets, variables y columnas |
| **Ignorados (Skip)** | `LINE_COMMENT` | `'//' ~[\r\n]* -> skip` | Comentario de una línea |
| | `BLOCK_COMMENT`| `'/*' .*? '*/' -> skip` | Comentario multilínea |
| | `WS` | `[ \t\r\n]+ -> skip` | Espacios, tabuladores y saltos de línea |
| **Error Léxico** | `ERROR_CHAR` | `.` | Cualquier carácter no reconocido |

---

## 3. Estructura del Repositorio
```text
.
├── VizFlowLexer.g4          # Gramática léxica en ANTLR4
├── Makefile                 # Automatización de generación y limpieza
├── main.py                  # Driver principal de análisis léxico
├── run_tests.py             # Ejecutor automatizado de pruebas
├── VizFlowLexer.py          # Código Python generado por ANTLR4
├── VizFlowLexer.tokens      # Tabla de tokens generada
├── VizFlowLexer.interp      # Intérprete ANTLR
├── README.md                # Documentación completa y especificación
├── TP-COMPILADORES.pdf      # Borrador del Informe del Trabajo Parcial
├── tests/                   # Suite de casos de prueba
│   ├── test_01_load.vf
│   ├── test_02_filter.vf
│   ├── test_03_transform.vf
│   ├── test_04_groupby.vf
│   ├── test_05_plot.vf
│   ├── test_06_pipeline_completo.vf
│   ├── test_07_comentarios.vf
│   └── test_08_error_lexico.vf
└── .gitignore               # Exclusión de archivos binarios y temporales
```

---

## 4. Instrucciones de Compilación y Ejecución

### Requisitos Previos
* **Python 3.10+**
* **Java 11+**
* Paquete Python runtime de ANTLR4:
  ```bash
  pip install antlr4-python3-runtime==4.13.1
  ```

### Compilar la Gramática Léxica
Para generar el archivo `VizFlowLexer.py` y sus dependencias a partir de `VizFlowLexer.g4`:
```bash
make all
```

Para limpiar los archivos generados:
```bash
make clean
```

### Ejecutar el Analizador Léxico sobre un Archivo
```bash
python3 main.py tests/test_06_pipeline_completo.vf
```

### Ejecutar Demostración Interactiva
```bash
python3 main.py --demo
```

### Ejecutar Suite Completa de Pruebas
```bash
python3 run_tests.py
```

---

## 5. Estrategia de Ramas Git
* `main`: Rama de producción y entregas del curso.
* `develop`: Integración y desarrollo continuo.
* `feature/analizador-lexico`: Desarrollo y validación del analizador léxico en ANTLR4.


## 6. Declaración del uso de IA

Durante el desarrollo de VizFlow se utilizaron herramientas de Inteligencia Artificial como apoyo en las siguientes actividades:

- **Analizador sintáctico (Parser):** Se utilizó IA como apoyo para revisar la estructura de las gramáticas, evitar ambigüedades y validar el manejo de la precedencia de operadores lógicos y aritméticos.

- **Analizador semántico:** Se utilizó IA como apoyo para plantear la estructura del analizador semántico, definir las principales validaciones semánticas y proponer casos de prueba para verificar su funcionamiento.

Las propuestas generadas con IA fueron revisadas, adaptadas y validadas por los integrantes del equipo antes de incorporarlas al proyecto.
