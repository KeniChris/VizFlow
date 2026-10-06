#!/usr/bin/env python3

"""
Ejecutor de pruebas automatizadas para los analizadores
léxico y sintáctico de VizFlow.

Pruebas léxicas:
- Los casos válidos deben ser reconocidos sin errores léxicos.
- Los casos de error deben detectar caracteres no reconocidos.

Pruebas sintácticas:
- Los casos válidos deben cumplir la gramática de VizFlow.
- Los casos inválidos deben producir al menos un error sintáctico.
"""

import os
import glob
import subprocess
import sys


# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================

def ejecutar_archivo(ruta):
    """
    Ejecuta main.py sobre un archivo .vf y devuelve
    el código de salida, stdout y stderr.
    """

    proceso = subprocess.run(
        [sys.executable, "main.py", ruta],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return proceso.returncode, proceso.stdout, proceso.stderr


# ============================================================================
# PRUEBAS DEL ANALIZADOR LÉXICO
# ============================================================================

def ejecutar_pruebas_lexicas():

    archivos_prueba = sorted(
        glob.glob("tests/test_lexico/*.vf")
    )

    print("\n" + "=" * 78)
    print("PRUEBAS DEL ANALIZADOR LÉXICO")
    print("=" * 78)

    if not archivos_prueba:
        print("[!] No se encontraron pruebas léxicas.")
        return 0, 0

    pasadas = 0
    total = len(archivos_prueba)

    for ruta in archivos_prueba:

        nombre = os.path.basename(ruta)

        # El archivo que contiene "error" en el nombre
        # representa un caso léxicamente inválido.
        es_caso_error = "error" in nombre.lower()

        codigo, salida, errores = ejecutar_archivo(ruta)

        if es_caso_error:

            # Esperamos que main.py termine con error y que
            # el lexer reporte los caracteres no reconocidos.
            if (
                codigo != 0
                and "DETALLE DE ERRORES LÉXICOS" in salida
            ):
                print(
                    f"[✓ PASS] {nombre:<35} "
                    f"-> Error léxico detectado correctamente."
                )
                pasadas += 1

            else:
                print(
                    f"[✗ FAIL] {nombre:<35} "
                    f"-> Se esperaba un error léxico."
                )

                if salida:
                    print(salida)

                if errores:
                    print(errores)

        else:

            # En una prueba léxica válida nos interesa comprobar
            # específicamente que el lexer no encuentre errores.
            if "Análisis léxico completado sin errores" in salida:

                print(
                    f"[✓ PASS] {nombre:<35} "
                    f"-> Tokens reconocidos correctamente."
                )
                pasadas += 1

            else:
                print(
                    f"[✗ FAIL] {nombre:<35} "
                    f"-> Falló el análisis léxico."
                )

                if salida:
                    print(salida)

                if errores:
                    print(errores)

    print("-" * 78)
    print(
        f"RESULTADO LÉXICO: "
        f"{pasadas}/{total} pruebas superadas."
    )

    return pasadas, total


# ============================================================================
# PRUEBAS SINTÁCTICAS - CASOS VÁLIDOS
# ============================================================================

def ejecutar_pruebas_sintacticas_validas():

    archivos_prueba = sorted(
        glob.glob("tests/test_sintactico/validos/*.vf")
    )

    print("\n" + "=" * 78)
    print("PRUEBAS DEL ANALIZADOR SINTÁCTICO - CASOS VÁLIDOS")
    print("=" * 78)

    if not archivos_prueba:
        print("[!] No se encontraron casos sintácticos válidos.")
        return 0, 0

    pasadas = 0
    total = len(archivos_prueba)

    for ruta in archivos_prueba:

        nombre = os.path.basename(ruta)

        codigo, salida, errores = ejecutar_archivo(ruta)

        # Un caso válido debe:
        # 1. No presentar errores léxicos.
        # 2. No presentar errores sintácticos.
        # 3. Terminar con código de salida 0.
        if (
            codigo == 0
            and "Análisis léxico completado sin errores" in salida
            and "Análisis sintáctico completado sin errores" in salida
        ):
            print(
                f"[✓ PASS] {nombre:<35} "
                f"-> Sintaxis válida."
            )
            pasadas += 1

        else:
            print(
                f"[✗ FAIL] {nombre:<35} "
                f"-> Se esperaba una sintaxis válida."
            )

            if salida:
                print(salida)

            if errores:
                print(errores)

    print("-" * 78)
    print(
        f"RESULTADO SINTÁCTICO (VÁLIDOS): "
        f"{pasadas}/{total} pruebas superadas."
    )

    return pasadas, total


# ============================================================================
# PRUEBAS SINTÁCTICAS - CASOS INVÁLIDOS
# ============================================================================

def ejecutar_pruebas_sintacticas_invalidas():

    archivos_prueba = sorted(
        glob.glob("tests/test_sintactico/invalidos/*.vf")
    )

    print("\n" + "=" * 78)
    print("PRUEBAS DEL ANALIZADOR SINTÁCTICO - CASOS INVÁLIDOS")
    print("=" * 78)

    if not archivos_prueba:
        print("[!] No se encontraron casos sintácticos inválidos.")
        return 0, 0

    pasadas = 0
    total = len(archivos_prueba)

    for ruta in archivos_prueba:

        nombre = os.path.basename(ruta)

        codigo, salida, errores = ejecutar_archivo(ruta)

        # El caso debe ser léxicamente correcto, pero
        # sintácticamente incorrecto.
        lexico_correcto = (
            "Análisis léxico completado sin errores" in salida
        )

        sintactico_incorrecto = (
            "Análisis sintáctico finalizado con errores" in salida
        )

        if (
            codigo != 0
            and lexico_correcto
            and sintactico_incorrecto
        ):
            print(
                f"[✓ PASS] {nombre:<35} "
                f"-> Error sintáctico detectado correctamente."
            )
            pasadas += 1

        else:
            print(
                f"[✗ FAIL] {nombre:<35} "
                f"-> Se esperaba un error sintáctico."
            )

            if salida:
                print(salida)

            if errores:
                print(errores)

    print("-" * 78)
    print(
        f"RESULTADO SINTÁCTICO (INVÁLIDOS): "
        f"{pasadas}/{total} pruebas superadas."
    )

    return pasadas, total


# ============================================================================
# EJECUCIÓN GENERAL
# ============================================================================

def ejecutar_pruebas():

    print("\n" + "=" * 78)
    print("SUITE DE PRUEBAS AUTOMATIZADAS - VIZFLOW")
    print("=" * 78)

    # ------------------------------------------------------------------------
    # 1. Pruebas léxicas
    # ------------------------------------------------------------------------

    lexico_pasadas, lexico_total = ejecutar_pruebas_lexicas()

    # ------------------------------------------------------------------------
    # 2. Pruebas sintácticas válidas
    # ------------------------------------------------------------------------

    sint_validas_pasadas, sint_validas_total = (
        ejecutar_pruebas_sintacticas_validas()
    )

    # ------------------------------------------------------------------------
    # 3. Pruebas sintácticas inválidas
    # ------------------------------------------------------------------------

    sint_invalidas_pasadas, sint_invalidas_total = (
        ejecutar_pruebas_sintacticas_invalidas()
    )

    # ------------------------------------------------------------------------
    # Resultado general
    # ------------------------------------------------------------------------

    total_pasadas = (
        lexico_pasadas
        + sint_validas_pasadas
        + sint_invalidas_pasadas
    )

    total_pruebas = (
        lexico_total
        + sint_validas_total
        + sint_invalidas_total
    )

    print("\n" + "=" * 78)
    print("RESULTADO GENERAL")
    print("=" * 78)

    print(
        f"Analizador léxico:              "
        f"{lexico_pasadas}/{lexico_total}"
    )

    print(
        f"Sintáctico - casos válidos:     "
        f"{sint_validas_pasadas}/{sint_validas_total}"
    )

    print(
        f"Sintáctico - casos inválidos:   "
        f"{sint_invalidas_pasadas}/{sint_invalidas_total}"
    )

    print("-" * 78)

    print(
        f"TOTAL: {total_pasadas}/{total_pruebas} "
        f"pruebas superadas."
    )

    print("=" * 78)

    # Código 0 solamente si todas las pruebas fueron superadas.
    return 0 if total_pasadas == total_pruebas else 1


if __name__ == '__main__':
    sys.exit(ejecutar_pruebas())
