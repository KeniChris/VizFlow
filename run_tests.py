#!/usr/bin/env python3

"""
Ejecutor de pruebas automatizadas para los analizadores
léxico, sintáctico y semántico de VizFlow.

Pruebas léxicas:
- Los casos válidos deben ser reconocidos sin errores léxicos.
- Los casos de error deben detectar caracteres no reconocidos.

Pruebas sintácticas:
- Los casos válidos deben cumplir la gramática de VizFlow.
- Los casos inválidos deben producir al menos un error sintáctico.
"""

import argparse
import json
import os
import glob
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================

def ejecutar_archivo(ruta, semantico=False):
    """
    Ejecuta main.py sobre un archivo .vf y devuelve
    el código de salida, stdout y stderr.
    """

    comando = [sys.executable, str(PROJECT_ROOT / "main.py")]
    if semantico:
        comando += ["--semantico", "--json"]
    comando.append(str(ruta))
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    proceso = subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=PROJECT_ROOT,
        env=entorno
    )

    return proceso.returncode, proceso.stdout, proceso.stderr


# ============================================================================
# PRUEBAS DEL ANALIZADOR LÉXICO
# ============================================================================

def ejecutar_pruebas_lexicas():

    archivos_prueba = sorted(
        glob.glob(str(PROJECT_ROOT / "tests/test_lexico/*.vf"))
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
        glob.glob(str(PROJECT_ROOT / "tests/test_sintactico/validos/*.vf"))
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
        glob.glob(str(PROJECT_ROOT / "tests/test_sintactico/invalidos/*.vf"))
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
# PRUEBAS SEMÁNTICAS DESDE PROGRAMAS FUENTE
# ============================================================================

def ejecutar_pruebas_semanticas():
    print("\n" + "=" * 78)
    print("PRUEBAS DEL ANALIZADOR SEMÁNTICO - ARCHIVOS .vf")
    print("=" * 78)
    pasadas = total = 0
    for grupo in ("validos", "invalidos"):
        carpeta = PROJECT_ROOT / "tests/test_semantico" / grupo
        archivos = sorted(carpeta.glob("*.vf"))
        if not archivos:
            print(f"[✗ FAIL] No hay entradas semánticas en {carpeta}.")
            total += 1
        for ruta in archivos:
            total += 1
            codigo, salida, errores = ejecutar_archivo(ruta, semantico=True)
            try:
                resultado = json.loads(salida)
                diagnosticos = resultado["diagnosticos"]
                if grupo == "validos":
                    correcta = codigo == 0 and resultado["ok"] and not diagnosticos
                    esperado = "Aceptado"
                else:
                    # Los nombres sem003_... documentan el diagnóstico esperado.
                    esperado = ruta.stem.split("_", 1)[0].upper()
                    correcta = (
                        codigo == 1 and not resultado["ok"]
                        and all(d["phase"] == "semántico" for d in diagnosticos)
                        and any(d["code"] == esperado for d in diagnosticos))
            except (ValueError, KeyError, TypeError):
                correcta = False
                esperado = "Respuesta semántica en JSON"
            etiqueta = "✓ PASS" if correcta else "✗ FAIL"
            print(f"[{etiqueta}] {ruta.name:<42} -> {esperado}")
            if correcta:
                pasadas += 1
            else:
                print(f"Código de salida: {codigo}\n{salida}{errores}")
    print(f"RESULTADO SEMÁNTICO: {pasadas}/{total} pruebas superadas.")
    return pasadas, total


def ejecutar_pruebas_unitarias():
    print("\n" + "=" * 78)
    print("PRUEBAS DE SEMÁNTICA, TABLA DE SÍMBOLOS E INTEGRACIÓN")
    print("=" * 78)
    suite = unittest.defaultTestLoader.discover(
        str(PROJECT_ROOT / "tests/test_semantico"), pattern="test_*.py")
    resultado = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    # Los subcasos no incrementan testsRun: un método con algún fallo cuenta
    # como una prueba fallida, aunque más de un subcaso haya fallado.
    fallidas = {caso.id() for caso, _ in resultado.failures + resultado.errors}
    for caso, _ in resultado.skipped + resultado.expectedFailures:
        fallidas.add(caso.id())
    fallidas.update(caso.id() for caso in resultado.unexpectedSuccesses)
    metodos = {identificador.split(" (", 1)[0] for identificador in fallidas}
    total = resultado.testsRun
    if total == 0:
        print("[✗ FAIL] No se encontraron pruebas unitarias.")
        return 0, 1
    return total - len(metodos), total


# ============================================================================
# EJECUCIÓN GENERAL
# ============================================================================

def ejecutar_pruebas(solo_originales=False):

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
    # 4. Pruebas semánticas y de integración
    # ------------------------------------------------------------------------

    semantico_pasadas = semantico_total = 0
    unitarias_pasadas = unitarias_total = 0
    if not solo_originales:
        semantico_pasadas, semantico_total = ejecutar_pruebas_semanticas()
        unitarias_pasadas, unitarias_total = ejecutar_pruebas_unitarias()

    total_pasadas = (
        lexico_pasadas
        + sint_validas_pasadas
        + sint_invalidas_pasadas
        + semantico_pasadas
        + unitarias_pasadas
    )

    total_pruebas = (
        lexico_total
        + sint_validas_total
        + sint_invalidas_total
        + semantico_total
        + unitarias_total
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

    if not solo_originales:
        print(f"Semántico - archivos .vf:       {semantico_pasadas}/{semantico_total}")
        print(f"Semántica e integración:        {unitarias_pasadas}/{unitarias_total}")

    print(
        f"TOTAL: {total_pasadas}/{total_pruebas} "
        f"pruebas superadas."
    )

    print("=" * 78)


    return 0 if total_pasadas == total_pruebas else 1


if __name__ == '__main__':
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")
    argumentos = argparse.ArgumentParser(description="Pruebas de las tres fases de VizFlow")
    argumentos.add_argument("--solo-originales", action="store_true",
                            help="Ejecutar únicamente las 21 pruebas léxicas y sintácticas")
    sys.exit(ejecutar_pruebas(argumentos.parse_args().solo_originales))
