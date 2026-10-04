lexer grammar VizFlowLexer;

/*
 * ============================================================================
 * Proyecto: Compilador del Lenguaje VizFlow (UPC - Teoría de Compiladores)
 * Analizador Léxico para VizFlow (DSL para Análisis y Visualización de Datos)
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 1. PALABRAS RESERVADAS (Keywords)
// NOTA IMPORTANTE: Deben definirse ANTES de la regla ID para tener prioridad.
// ----------------------------------------------------------------------------

// Comandos y estructuras principales
DATASET     : 'DATASET' ;
LOAD        : 'LOAD' ;
FILTER      : 'FILTER' ;
TRANSFORM   : 'TRANSFORM' ;
GROUP_BY    : 'GROUP_BY' ;
PLOT        : 'PLOT' ;
DASHBOARD   : 'DASHBOARD' ;

// Funciones estadísticas de agregación
SUM         : 'SUM' ;
AVG         : 'AVG' ;
MIN         : 'MIN' ;
MAX         : 'MAX' ;
COUNT       : 'COUNT' ;

// Tipos de visualización soportados en sentencias PLOT
BAR         : 'BAR' ;
LINE        : 'LINE' ;
SCATTER     : 'SCATTER' ;

// Constantes y literales lógicos
TRUE        : 'true' | 'TRUE' ;
FALSE       : 'false' | 'FALSE' ;
NULL        : 'null' | 'NULL' ;

// Operadores lógicos textuales
AND         : 'and' | 'AND' ;
OR          : 'or' | 'OR' ;
NOT         : 'not' | 'NOT' ;


// ----------------------------------------------------------------------------
// 2. OPERADOR DE TUBERÍA (Pipeline Operator)
// ----------------------------------------------------------------------------
PIPE        : '|>' ;


// ----------------------------------------------------------------------------
// 3. OPERADORES RELACIONALES / DE COMPARACIÓN
// NOTA: Los operadores de dos caracteres deben ir antes de los de un carácter.
// ----------------------------------------------------------------------------
EQ          : '==' ;
NEQ         : '!=' ;
LTE         : '<=' ;
GTE         : '>=' ;
LT          : '<' ;
GT          : '>' ;


// ----------------------------------------------------------------------------
// 4. OPERADORES DE ASIGNACIÓN
// ----------------------------------------------------------------------------
ASSIGN      : '=' ;


// ----------------------------------------------------------------------------
// 5. OPERADORES ARITMÉTICOS
// ----------------------------------------------------------------------------
PLUS        : '+' ;
MINUS       : '-' ;
STAR        : '*' ;
SLASH       : '/' ;
MOD         : '%' ;


// ----------------------------------------------------------------------------
// 6. OPERADORES LÓGICOS SIMBÓLICOS
// ----------------------------------------------------------------------------
AND_OP      : '&&' ;
OR_OP       : '||' ;
NOT_OP      : '!' ;


// ----------------------------------------------------------------------------
// 7. SIGNOS DE PUNTUACIÓN Y DELIMITADORES
// ----------------------------------------------------------------------------
LPAREN      : '(' ;
RPAREN      : ')' ;
COMMA       : ',' ;
SEMI        : ';' ;


// ----------------------------------------------------------------------------
// 8. LITERALES (Literals)
// Reglas más específicas primero (FLOAT_LIT antes de INT_LIT).
// ----------------------------------------------------------------------------

// Literales de cadena entre comillas dobles (soporta secuencias de escape)
STRING_LIT  : '"' (~["\r\n\\] | '\\' .)* '"' ;

// Literales numéricos en punto flotante (con o sin notación científica)
FLOAT_LIT   : DIGITOS '.' DIGITOS? EXPONENTE?
            | '.' DIGITOS EXPONENTE?
            | DIGITOS EXPONENTE
            ;

// Literales numéricos enteros
INT_LIT     : DIGITOS ;


// ----------------------------------------------------------------------------
// 9. IDENTIFICADORES (Identifiers)
// Nombres de datasets, variables y columnas (ej. ventas, monto, categoria).
// ----------------------------------------------------------------------------
ID          : [a-zA-Z_] [a-zA-Z0-9_]* ;


// ----------------------------------------------------------------------------
// 10. ELEMENTOS A IGNORAR (Espacios en blanco y comentarios)
// Se procesan con directiva '-> skip' según el estilo de ANTLR4.
// ----------------------------------------------------------------------------

// Comentario de una sola línea (inicia con // hasta fin de línea)
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;

// Comentario de bloque multilínea (/* ... */)
// El cuantificador '.*?' no codicioso detiene la captura en el primer '*/'
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

// Espacios en blanco, tabulaciones y saltos de línea
WS            : [ \t\r\n]+ -> skip ;


// ----------------------------------------------------------------------------
// 11. MANEJO DE ERRORES LÉXICOS / CARACTERES DESCONOCIDOS
// Al colocar '.' al final, cualquier carácter no válido es capturado como
// token ERROR_CHAR para ser reportado por el analizador sin interrumpir el flujo.
// ----------------------------------------------------------------------------
ERROR_CHAR  : . ;


// ----------------------------------------------------------------------------
// FRAGMENTOS AUXILIARES (Reutilizables, no producen tokens individuales)
// ----------------------------------------------------------------------------
fragment DIGITO    : [0-9] ;
fragment DIGITOS   : DIGITO+ ;
fragment SIGNO     : [+\-] ;
fragment EXPONENTE : [eE] SIGNO? DIGITOS ;
