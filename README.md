# VizFlow - Compilador para Análisis y Visualización de Datos

## Información del Proyecto
* **Curso:** 1ACC0218 - Teoría de Compiladores (UPC)
* **Sección:** 4889
* **Docente:** José Luis Soncco Álvarez
* **Integrantes del Grupo:**
  * Pamela Rivera Contreras (U202216662)
  * Piero Antonio Aguilar Anticona (U202419995)
  * Leicy Cristell Cahuana López (U20231E777)


## Descripción de la solución

VizFlow es un lenguaje de dominio específico para organizar, analizar y visualizar datos CSV de manera secuencial y legible. Permite declarar datasets y encadenar filtros, transformaciones, agrupaciones y gráficos mediante el operador `|>`.

Esta versión implementa el análisis léxico, sintáctico y semántico, la construcción del AST y la gestión de la tabla de símbolos. El repositorio incluye las gramáticas, el compilador, datos de ejemplo y pruebas automatizadas.

## Tecnologías

- Python 3.10 o superior.
- ANTLR 4.13.1.
- Java 11 o superior para regenerar el lexer y el parser.

## Ejecución básica

```bash
python3 -m pip install -r requirements.txt
python3 main.py --semantico examples/valido.vf
python3 run_tests.py
```

## Declaración del uso de IA

Se utilizó IA como apoyo para revisar las gramáticas, estructurar el analizador semántico y proponer pruebas. Las propuestas fueron revisadas, adaptadas y validadas por los integrantes del equipo.
