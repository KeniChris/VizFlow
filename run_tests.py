#!/usr/bin/env python3
"""
Ejecutor de pruebas automatizadas para el analizador léxico de VizFlow.
Verifica que los casos de prueba válidos pasen sin errores
y que los casos inválidos detecten los errores léxicos esperados.
"""

import os
import glob
import subprocess
import sys


def ejecutar_pruebas():
    archivos_prueba = sorted(glob.glob("tests/test_*.vf"))
    if not archivos_prueba:
        print("No se encontraron archivos de prueba en tests/")
        return 1

    total = len(archivos_prueba)
    pasadas = 0

    print("=" * 70)
    print("SUITE DE PRUEBAS AUTOMATIZADAS - ANALIZADOR LÉXICO VIZFLOW")
    print("=" * 70)

    for ruta in archivos_prueba:
        nombre = os.path.basename(ruta)
        es_caso_error = "error" in nombre

        proceso = subprocess.run(
            [sys.executable, "main.py", ruta],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        salida = proceso.stdout

        if es_caso_error:
            # Esperamos que falle el código de salida y reporte errores léxicos
            if proceso.returncode != 0 and "DETALLE DE ERRORES LÉXICOS" in salida:
                print(f"[✓ PASS] {nombre:<30} -> Error léxico detectado correctamente.")
                pasadas += 1
            else:
                print(f"[✗ FAIL] {nombre:<30} -> Se esperaba detección de error léxico pero pasó.")
        else:
            # Esperamos que termine con código 0 y sin errores
            if proceso.returncode == 0 and "Análisis léxico completado sin errores" in salida:
                print(f"[✓ PASS] {nombre:<30} -> Todos los tokens reconocidos con éxito.")
                pasadas += 1
            else:
                print(f"[✗ FAIL] {nombre:<30} -> Falló el análisis en archivo válido.")
                print(salida)

    print("=" * 70)
    print(f"RESULTADO: {pasadas}/{total} pruebas superadas.")
    print("=" * 70)

    return 0 if pasadas == total else 1


if __name__ == '__main__':
    sys.exit(ejecutar_pruebas())
