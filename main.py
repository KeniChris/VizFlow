#!/usr/bin/env python3
"""
Driver principal para el analizador léxico de VizFlow.
Basado en las directrices de la Unidad I (Análisis Léxico) del curso
Teoría de Compiladores (UPC).
"""

import sys
from antlr4 import CommonTokenStream, FileStream, InputStream, Token
from gen.VizFlowLexer import VizFlowLexer


# Clasificación de tokens para resumen estadístico
KEYWORDS = {
    'DATASET', 'LOAD', 'FILTER', 'TRANSFORM', 'GROUP_BY', 'PLOT', 'DASHBOARD',
    'SUM', 'AVG', 'MIN', 'MAX', 'COUNT', 'BAR', 'LINE', 'SCATTER',
    'TRUE', 'FALSE', 'NULL', 'AND', 'OR', 'NOT'
}

OPERATORS = {
    'PIPE', 'EQ', 'NEQ', 'LTE', 'GTE', 'LT', 'GT', 'ASSIGN',
    'PLUS', 'MINUS', 'STAR', 'SLASH'
}

DELIMITERS = {'LPAREN', 'RPAREN', 'COMMA', 'SEMI'}

LITERALS = {'STRING_LIT', 'FLOAT_LIT', 'INT_LIT'}


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

        print(f"{posicion:<12} | {nombre_token:<20} | {lexema_repr:<40}")

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
            errores.append((token.line, token.column, token.text))

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
            print(f"    - Línea {linea}, Columna {col}: Carácter no reconocido {repr(char)}")
        print("=" * 78)
        return False
    else:
        print("\n[✓] Análisis léxico completado sin errores.")
        print("=" * 78)
        return True


def analizar_archivo(ruta_archivo: str) -> bool:
    """Ejecuta el análisis léxico sobre un archivo fuente."""
    print(f"\nIniciando análisis léxico del archivo: '{ruta_archivo}'\n")
    try:
        entrada = FileStream(ruta_archivo, encoding='utf-8')
    except Exception as e:
        print(f"Error al abrir el archivo '{ruta_archivo}': {e}", file=sys.stderr)
        return False

    lexer = VizFlowLexer(entrada)
    stream = CommonTokenStream(lexer)
    stream.fill()

    return mostrar_tokens(stream, lexer)


def analizar_cadena(codigo: str) -> bool:
    """Ejecuta el análisis léxico sobre una cadena en memoria."""
    entrada = InputStream(codigo)
    lexer = VizFlowLexer(entrada)
    stream = CommonTokenStream(lexer)
    stream.fill()

    return mostrar_tokens(stream, lexer)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo.vf>")
        print("     python3 main.py --demo (ejecuta un ejemplo predeterminado)")
        sys.exit(1)

    param = sys.argv[1]
    if param == '--demo':
        demo_code = (
            'DATASET ventas = LOAD "ventas.csv";\n'
            'ventas\n'
            '  |> FILTER(monto > 500 AND categoria != "descontinuado")\n'
            '  |> TRANSFORM(monto_igv = monto * 1.18)\n'
            '  |> GROUP_BY(categoria, SUM(monto))\n'
            '  |> PLOT BAR(x=categoria, y=monto)\n'
            '  |> DASHBOARD;\n'
        )
        print("Ejecutando demostración con código VizFlow predeterminado:\n")
        print(demo_code)
        exito = analizar_cadena(demo_code)
    else:
        exito = analizar_archivo(param)

    sys.exit(0 if exito else 1)


if __name__ == '__main__':
    main()
