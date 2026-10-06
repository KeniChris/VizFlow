lexer grammar VizFlowLexer;

/*
 * ============================================================================
 * Proyecto: Compilador del Lenguaje VizFlow (UPC - Teoría de Compiladores)
 * Analizador Léxico para VizFlow (DSL para Análisis y Visualización de Datos)
 * ============================================================================
 */


// ----------------------------------------------------------------------------
// 1. PALABRAS RESERVADAS (Keywords)
// Se definen antes de la regla ID para que ANTLR las reconozca como palabras
// reservadas y no como identificadores.
// ----------------------------------------------------------------------------

// Comandos y construcciones principales del lenguaje
DATASET     : 'DATASET' ;
LOAD        : 'LOAD' ;
FILTER      : 'FILTER' ;
TRANSFORM   : 'TRANSFORM' ;
GROUP_BY    : 'GROUP_BY' ;
PLOT        : 'PLOT' ;
DASHBOARD   : 'DASHBOARD' ;

// Funciones estadísticas utilizadas en operaciones de agrupamiento
SUM         : 'SUM' ;
AVG         : 'AVG' ;
MIN         : 'MIN' ;
MAX         : 'MAX' ;
COUNT       : 'COUNT' ;

// Tipos de visualización soportados por PLOT
BAR         : 'BAR' ;
LINE        : 'LINE' ;
SCATTER     : 'SCATTER' ;

// Parámetros utilizados en PLOT
X           : 'x' | 'X' ;
Y           : 'y' | 'Y' ;

// Valores booleanos y valor nulo
TRUE        : 'true' | 'TRUE' ;
FALSE       : 'false' | 'FALSE' ;
NULL        : 'null' | 'NULL' ;

// Operadores lógicos textuales utilizados en condiciones de FILTER
AND         : 'and' | 'AND' ;
OR          : 'or' | 'OR' ;
NOT         : 'not' | 'NOT' ;


// ----------------------------------------------------------------------------
// 2. OPERADOR DE TUBERÍA (Pipeline Operator)
// Permite encadenar operaciones de forma secuencial sobre un mismo dataset.
// ----------------------------------------------------------------------------

PIPE        : '|>' ;


// ----------------------------------------------------------------------------
// 3. OPERADORES RELACIONALES / DE COMPARACIÓN
// Los operadores de dos caracteres se definen antes que los de un carácter.
// Se utilizan principalmente en las condiciones de FILTER.
// ----------------------------------------------------------------------------

EQ          : '==' ;
NEQ         : '!=' ;
LTE         : '<=' ;
GTE         : '>=' ;
LT          : '<' ;
GT          : '>' ;


// ----------------------------------------------------------------------------
// 4. OPERADOR DE ASIGNACIÓN
// Se utiliza en la declaración de datasets y en las transformaciones.
// ----------------------------------------------------------------------------

ASSIGN      : '=' ;


// ----------------------------------------------------------------------------
// 5. OPERADORES ARITMÉTICOS
// Permiten construir expresiones aritméticas dentro de TRANSFORM.
// La precedencia de estos operadores será definida por la gramática sintáctica.
// ----------------------------------------------------------------------------

PLUS        : '+' ;
MINUS       : '-' ;
STAR        : '*' ;
SLASH       : '/' ;


// ----------------------------------------------------------------------------
// 6. SIGNOS DE PUNTUACIÓN Y DELIMITADORES
// Los paréntesis también permiten agrupar expresiones y condiciones.
// ----------------------------------------------------------------------------

LPAREN      : '(' ;
RPAREN      : ')' ;
COMMA       : ',' ;
SEMI        : ';' ;


// ----------------------------------------------------------------------------
// 7. LITERALES (Literals)
// FLOAT_LIT se define antes de INT_LIT por ser una regla más específica.
// ----------------------------------------------------------------------------

// Literales de cadena entre comillas dobles.
// Permite caracteres escapados dentro de la cadena.
STRING_LIT  : '"' (~["\r\n\\] | '\\' .)* '"' ;

// Literales numéricos de punto flotante.
// Se permiten valores decimales y notación científica.
FLOAT_LIT   : DIGITOS '.' DIGITOS? EXPONENTE?
            | '.' DIGITOS EXPONENTE?
            | DIGITOS EXPONENTE
            ;

// Literales numéricos enteros
INT_LIT     : DIGITOS ;


// ----------------------------------------------------------------------------
// 8. IDENTIFICADORES (Identifiers)
// Representan nombres de datasets, columnas y nuevos valores generados
// mediante transformaciones.
// ----------------------------------------------------------------------------

ID          : [a-zA-Z_] [a-zA-Z0-9_]* ;


// ----------------------------------------------------------------------------
// 9. ELEMENTOS A IGNORAR (Espacios en blanco y comentarios)
// Estos elementos no intervienen en la estructura sintáctica del programa,
// por lo que se procesan mediante la directiva -> skip.
// ----------------------------------------------------------------------------

// Comentario de una sola línea: // comentario
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;

// Comentario multilínea: /* comentario */
// El cuantificador no codicioso .*? finaliza en la primera aparición de */
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

// Espacios en blanco, tabulaciones y saltos de línea
WS            : [ \t\r\n]+ -> skip ;


// ----------------------------------------------------------------------------
// 10. MANEJO DE ERRORES LÉXICOS / CARACTERES DESCONOCIDOS
// Al ubicarse al final, captura cualquier carácter que no corresponda con
// alguno de los tokens definidos anteriormente.
// ----------------------------------------------------------------------------

ERROR_CHAR    : . ;


// ----------------------------------------------------------------------------
// FRAGMENTOS AUXILIARES
// Se utilizan para construir otros tokens y no generan tokens por sí mismos.
// ----------------------------------------------------------------------------

fragment DIGITO    : [0-9] ;
fragment DIGITOS   : DIGITO+ ;
fragment SIGNO     : [+\-] ;
fragment EXPONENTE : [eE] SIGNO? DIGITOS ;
