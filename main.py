#!/usr/bin/env python3

"""
Driver principal para los analizadores léxico y sintáctico de VizFlow.

Basado en las directrices de la Unidad I del curso
Teoría de Compiladores (UPC).
"""

import sys

from antlr4 import CommonTokenStream, FileStream, InputStream, Token

from gen.VizFlowLexer import VizFlowLexer
from gen.VizFlowParser import VizFlowParser


# ============================================================================
# CLASIFICACIÓN DE TOKENS
# ============================================================================

KEYWORDS = {
    'DATASET', 'LOAD', 'FILTER', 'TRANSFORM', 'GROUP_BY', 'PLOT', 'DASHBOARD',
    'SUM', 'AVG', 'MIN', 'MAX', 'COUNT',
    'BAR', 'LINE', 'SCATTER',
    'X', 'Y',
    'TRUE', 'FALSE', 'NULL',
    'AND', 'OR', 'NOT'
}

OPERATORS = {
    'PIPE', 'EQ', 'NEQ', 'LTE', 'GTE', 'LT', 'GT', 'ASSIGN',
    'PLUS', 'MINUS', 'STAR', 'SLASH'
}

DELIMITERS = {
    'LPAREN', 'RPAREN', 'COMMA', 'SEMI'
}

LITERALS = {
    'STRING_LIT', 'FLOAT_LIT', 'INT_LIT'
}


# ============================================================================
# ANÁLISIS LÉXICO
# ============================================================================

def mostrar_tokens(stream, lexer):
    """
    Recorre el flujo de tokens generado por el Lexer y muestra
    cada token con su posición (línea:columna), nombre simbólico y lexema.
    """

    total_tokens = 0
    conteo_keywords = 0
    conteo_operadores = 0
    conteo_literales = 0
    conteo_ids = 0
    conteo_delimitadores = 0
    errores = []

    print("=" * 78)
    print(f"{'POSICIÓN':<12} | {'TIPO DE TOKEN':<20} | {'LEXEMA':<40}")
    print("-" * 78)

    for token in stream.tokens:

        if token.type == Token.EOF:
            continue

        nombre_token = lexer.symbolicNames[token.type]

        if nombre_token is None:
            nombre_token = f"TOKEN_{token.type}"

        posicion = f"[{token.line}:{token.column}]"
        lexema_repr = repr(token.text)

        print(
            f"{posicion:<12} | "
            f"{nombre_token:<20} | "
            f"{lexema_repr:<40}"
        )

        total_tokens += 1

        if nombre_token in KEYWORDS:
            conteo_keywords += 1

        elif nombre_token in OPERATORS:
            conteo_operadores += 1

        elif nombre_token in DELIMITERS:
            conteo_delimitadores += 1

        elif nombre_token in LITERALS:
            conteo_literales += 1

        elif nombre_token == 'ID':
            conteo_ids += 1

        elif nombre_token == 'ERROR_CHAR':
            errores.append(
                (token.line, token.column, token.text)
            )

    print("=" * 78)
    print("RESUMEN DEL ANÁLISIS LÉXICO:")
    print(f"  * Total de tokens válidos:     {total_tokens - len(errores)}")
    print(f"  * Palabras reservadas (KW):    {conteo_keywords}")
    print(f"  * Identificadores (ID):        {conteo_ids}")
    print(f"  * Operadores (incluye pipe):   {conteo_operadores}")
    print(f"  * Literales (cadenas/números): {conteo_literales}")
    print(f"  * Delimitadores / signos:      {conteo_delimitadores}")
    print(f"  * Errores léxicos detectados:  {len(errores)}")

    if errores:

        print("\n[!] DETALLE DE ERRORES LÉXICOS:")

        for linea, col, char in errores:
            print(
                f"    - Línea {linea}, Columna {col}: "
                f"Carácter no reconocido {repr(char)}"
            )

        print("=" * 78)
        return False

    print("\n[✓] Análisis léxico completado sin errores.")
    print("=" * 78)

    return True


# ============================================================================
# ANÁLISIS SINTÁCTICO
# ============================================================================

def analizar_sintaxis(stream):
    """
    Ejecuta el análisis sintáctico utilizando la regla 'programa'
    definida como regla inicial en VizFlowParser.g4.
    """

    parser = VizFlowParser(stream)

    # Inicia el análisis desde la regla principal de la gramática.
    parser.programa()

    errores = parser.getNumberOfSyntaxErrors()

    print("\n" + "=" * 78)
    print("RESUMEN DEL ANÁLISIS SINTÁCTICO:")

    if errores > 0:
        print(f"  * Errores sintácticos detectados: {errores}")
        print("\n[!] Análisis sintáctico finalizado con errores.")
        print("=" * 78)

        return False

    print("  * Errores sintácticos detectados: 0")
    print("\n[✓] Análisis sintáctico completado sin errores.")
    print("=" * 78)

    return True


# ============================================================================
# ANÁLISIS DE ARCHIVO
# ============================================================================

def analizar_archivo(ruta_archivo: str) -> bool:
    """
    Ejecuta el análisis léxico y sintáctico sobre un archivo fuente.
    """

    print(f"\nIniciando análisis del archivo: '{ruta_archivo}'\n")

    try:
        entrada = FileStream(
            ruta_archivo,
            encoding='utf-8'
        )

    except Exception as e:
        print(
            f"Error al abrir el archivo '{ruta_archivo}': {e}",
            file=sys.stderr
        )
        return False

    # ------------------------------------------------------------------------
    # 1. Análisis léxico
    # ------------------------------------------------------------------------

    lexer = VizFlowLexer(entrada)
    stream = CommonTokenStream(lexer)

    # Generamos todos los tokens.
    stream.fill()

    lexico_correcto = mostrar_tokens(
        stream,
        lexer
    )

    # Si existen errores léxicos, no continuamos con el parser.
    if not lexico_correcto:
        return False

    # ------------------------------------------------------------------------
    # 2. Análisis sintáctico
    # ------------------------------------------------------------------------

    # Regresamos al inicio del flujo de tokens para que el parser
    # pueda recorrerlo desde el primer token.
    stream.seek(0)

    return analizar_sintaxis(stream)


# ============================================================================
# ANÁLISIS DE CADENA
# ============================================================================

def analizar_cadena(codigo: str) -> bool:
    """
    Ejecuta el análisis léxico y sintáctico sobre una cadena en memoria.
    """

    entrada = InputStream(codigo)

    # ------------------------------------------------------------------------
    # 1. Análisis léxico
    # ------------------------------------------------------------------------

    lexer = VizFlowLexer(entrada)
    stream = CommonTokenStream(lexer)

    stream.fill()

    lexico_correcto = mostrar_tokens(
        stream,
        lexer
    )

    if not lexico_correcto:
        return False

    # ------------------------------------------------------------------------
    # 2. Análisis sintáctico
    # ------------------------------------------------------------------------

    stream.seek(0)

    return analizar_sintaxis(stream)


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():

    if len(sys.argv) < 2:

        print("Uso:")
        print("  python3 main.py <archivo.vf>")
        print("  python3 main.py --demo")

        sys.exit(1)

    param = sys.argv[1]

    # ------------------------------------------------------------------------
    # Demostración predeterminada
    # ------------------------------------------------------------------------

    if param == '--demo':

        demo_code = (
            'DATASET ventas = LOAD "ventas.csv";\n'
            '\n'
            'ventas\n'
            '  |> FILTER(monto > 500 AND categoria != "descontinuado")\n'
            '  |> TRANSFORM(monto_igv = monto * 1.18)\n'
            '  |> GROUP_BY(categoria, SUM(monto))\n'
            '  |> PLOT BAR(x=categoria, y=monto)\n'
            '  |> DASHBOARD;\n'
        )

        print(
            "Ejecutando demostración con código "
            "VizFlow predeterminado:\n"
        )

        print(demo_code)

        exito = analizar_cadena(demo_code)

    # ------------------------------------------------------------------------
    # Archivo proporcionado por el usuario
    # ------------------------------------------------------------------------

    else:
        exito = analizar_archivo(param)

    # Código de salida:
    # 0 = análisis correcto
    # 1 = se detectaron errores
    sys.exit(0 if exito else 1)


if __name__ == '__main__':
    main()
