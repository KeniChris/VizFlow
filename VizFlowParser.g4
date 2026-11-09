
parser grammar VizFlowParser;

/*
 * ============================================================================
 * Proyecto: Compilador del Lenguaje VizFlow (UPC - Teoría de Compiladores)
 * Analizador Sintáctico para VizFlow (DSL para Análisis y Visualización de Datos)
 * ============================================================================
 */

options {
    tokenVocab = VizFlowLexer;
}

// ----------------------------------------------------------------------------
// 1. REGLA INICIAL DEL PROGRAMA
// Un programa VizFlow contiene una o más sentencias.
// EOF asegura que todo el archivo sea procesado.
// ----------------------------------------------------------------------------
programa
    : sentencia listaSentencias EOF
    ;

listaSentencias
    : sentencia listaSentencias
    |
    ;

sentencia
    : declaracionDataset
    | pipeline
    ;

// ----------------------------------------------------------------------------
// 2. DECLARACIÓN Y CARGA DE DATASETS
// Permite declarar un dataset y cargar sus datos desde un archivo.
// Ejemplo: DATASET ventas = LOAD "ventas.csv";
// ----------------------------------------------------------------------------
declaracionDataset
    : DATASET ID ASSIGN LOAD STRING_LIT SEMI
    ;

// ----------------------------------------------------------------------------
// 3. PIPELINE GENERAL DE VIZFLOW
// Permite aplicar una o más operaciones sobre un dataset mediante |>.
// Las operaciones adicionales se definen mediante recursión.
// El pipeline puede finalizar opcionalmente con DASHBOARD.
// ----------------------------------------------------------------------------
pipeline
    : ID PIPE operacion operacionesAdicionales dashboardOpcional SEMI
    ;

operacionesAdicionales
    : PIPE operacion operacionesAdicionales
    |
    ;

dashboardOpcional
    : PIPE DASHBOARD
    |
    ;

operacion
    : filterOp
    | transformOp
    | groupByOp
    | plotOp
    ;

// ----------------------------------------------------------------------------
// 4. OPERACIÓN FILTER
// Permite filtrar registros mediante condiciones simples o compuestas.
// Precedencia lógica: NOT > AND > OR.
// ----------------------------------------------------------------------------
filterOp
    : FILTER LPAREN expresionLogica RPAREN
    ;

// Nivel de menor precedencia: OR
expresionLogica
    : expresionAnd continuacionOr
    ;

continuacionOr
    : OR expresionAnd continuacionOr
    |
    ;

// Nivel intermedio: AND
expresionAnd
    : expresionNot continuacionAnd
    ;

continuacionAnd
    : AND expresionNot continuacionAnd
    |
    ;

// Nivel de mayor precedencia lógica: NOT
expresionNot
    : NOT expresionNot
    | comparacion
    | LPAREN expresionLogica RPAREN
    ;

comparacion
    : ID operadorRelacional valor
    ;

operadorRelacional
    : EQ
    | NEQ
    | LT
    | GT
    | LTE
    | GTE
    ;

valor
    : ID
    | INT_LIT
    | FLOAT_LIT
    | STRING_LIT
    | TRUE
    | FALSE
    | NULL
    ;

// ----------------------------------------------------------------------------
// 5. OPERACIÓN TRANSFORM
// Permite crear una nueva columna mediante una expresión aritmética.
// Precedencia: paréntesis > multiplicación/división > suma/resta.
// ----------------------------------------------------------------------------
transformOp
    : TRANSFORM LPAREN ID ASSIGN expresionAritmetica RPAREN
    ;

// Nivel de menor precedencia: suma y resta
expresionAritmetica
    : termino continuacionSuma
    ;

continuacionSuma
    : PLUS termino continuacionSuma
    | MINUS termino continuacionSuma
    |
    ;

// Nivel de mayor precedencia aritmética: multiplicación y división
termino
    : factor continuacionProducto
    ;

continuacionProducto
    : STAR factor continuacionProducto
    | SLASH factor continuacionProducto
    |
    ;

// Elementos básicos y expresiones agrupadas
factor
    : LPAREN expresionAritmetica RPAREN
    | ID
    | INT_LIT
    | FLOAT_LIT
    ;

// ----------------------------------------------------------------------------
// 6. OPERACIÓN GROUP_BY
// Permite agrupar registros y aplicar una función de agregación.
// SUM, AVG, MIN y MAX reciben una columna; COUNT no recibe argumentos.
// ----------------------------------------------------------------------------
groupByOp
    : GROUP_BY LPAREN ID COMMA agregacion RPAREN
    ;

agregacion
    : funcionAgregacion LPAREN ID RPAREN
    | COUNT LPAREN RPAREN
    ;

funcionAgregacion
    : SUM
    | AVG
    | MIN
    | MAX
    ;

// ----------------------------------------------------------------------------
// 7. OPERACIÓN PLOT
// Permite generar gráficos BAR, LINE o SCATTER.
// Se indican las columnas correspondientes a los ejes X e Y.
// ----------------------------------------------------------------------------
plotOp
    : PLOT tipoGrafico LPAREN X ASSIGN ID COMMA Y ASSIGN ID RPAREN
    ;

tipoGrafico
    : BAR
    | LINE
    | SCATTER
    ;

