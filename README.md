# VizFlow - Compilador para Análisis y Visualización de Datos

## Información del Proyecto
* **Curso:** 1ACC0218 - Teoría de Compiladores (UPC)
* **Sección:** 4889
* **Docente:** José Luis Soncco Álvarez
* **Integrantes:**
  * Pamela Rivera Contreras (U202216662)
  * Piero Antonio Aguilar Anticona (U202419995)
  * Leicy Cristell Cahuana López (U20231E777)

---

## Descripción General
**VizFlow** es un lenguaje de programación de dominio específico (DSL) diseñado para facilitar el análisis exploratorio y la visualización de datos estructurados de manera declarativa y reproducible.

VizFlow introduce el operador de tubería (**`|>`**) para encadenar transformaciones de datos de forma limpia y directa:
1. Ingesta de datos tabulares (`LOAD`).
2. Filtrado relacional y lógico (`FILTER`).
3. Transformaciones y cálculo de columnas derivadas (`TRANSFORM`).
4. Agrupaciones y funciones estadísticas (`GROUP_BY`, `SUM`, `AVG`, `MIN`, `MAX`, `COUNT`).
5. Generación de gráficos (`PLOT BAR`, `PLOT LINE`, `PLOT SCATTER`).
6. Presentación de resultados y tableros interactivos (`DASHBOARD`).

---

## Estructura de Ramas
* **`main`**: Versión de producción y entregas oficiales (Hito 1, Hito 2, Hito 3).
* **`develop`**: Rama base de integración de desarrollo.
* **`feature/*`**: Ramas de funcionalidades específicas (ej. `feature/analizador-lexico`).
