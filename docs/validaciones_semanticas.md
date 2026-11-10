# Validaciones semánticas y gramática actual

La gramática decide qué programas llegan al analizador semántico. Hay 15 códigos
implementados, pero cuatro de ellos solo se alcanzan construyendo un AST directamente:
desde un archivo `.vf`, el parser rechaza antes esas construcciones con `SYN001`.

| Código | Validación | Resultado desde un `.vf` actual |
| --- | --- | --- |
| SEM001 | Dataset no declarado | SEM001 |
| SEM002 | Dataset declarado dos veces | SEM002 |
| SEM003 | Columna inexistente | SEM003 |
| SEM004 | Tipos incompatibles en expresiones y operaciones | SEM004 |
| SEM005 | FILTER requiere una condición BOOLEAN | El parser rechaza condiciones sin comparación: SYN001 |
| SEM006 | Aridad y argumentos de las agregaciones | El parser ya exige una columna o COUNT(): SYN001 |
| SEM007 | SUM, AVG, MIN y MAX requieren columnas numéricas | SEM007 |
| SEM008 | División por cero constante | SEM008 |
| SEM009 | Ejes y tipos de los gráficos | Los tipos incorrectos producen SEM009; la forma de los ejes también la restringe el parser |
| SEM010 | DASHBOARD debe cerrar la tubería | El parser ya exige ese orden: SYN001 |
| SEM011 | CSV inexistente, ilegible o con estructura incorrecta | SEM011 |
| SEM012 | Colisión de nombres en el resultado de GROUP_BY | SEM012 |
| SEM013 | Las agregaciones deben estar en GROUP_BY | El parser ya restringe su contexto: SYN001 |
| SEM014 | Uso de una columna sin inicialización válida | SEM014 después del error que impidió inicializarla |
| SEM015 | LOAD requiere una extensión .csv, sin distinguir mayúsculas | SEM015, con la extensión recibida y la ruta |

## Pruebas reproducibles

```bash
python3 run_tests.py
```

`tests/test_semantico/test_diagnostics.py` comprueba los diagnósticos exactos de
los 11 códigos observables desde fuentes `.vf`, las cuatro guardas mediante AST,
la fase sintáctica de sus equivalentes rechazados y operaciones válidas que no
deben activar las guardas. También prueba las formas de ejes que el parser impide.

Para ejecutar solo esta comprobación:

```bash
python3 -m unittest discover -s tests/test_semantico -p 'test_diagnostics.py' -v
```

## Ejemplo de SEM014

```text
DATASET ventas = LOAD "../../data/ventas.csv";
ventas |> GROUP_BY(region, SUM(categoria)) |> FILTER(categoria == "A");
```

`SUM(categoria)` produce `SEM007` porque la columna es texto. La columna de
salida queda sin una inicialización válida; usarla en el siguiente FILTER
produce `SEM014`. Este caso verifica ambos diagnósticos, en ese orden, y no
presenta SEM014 como un error independiente de la agregación fallida.

```bash
python3 main.py --semantico examples/errores/sem014_columna_no_inicializada.vf
```

## Ejemplo de SEM015

```text
DATASET ventas = LOAD "ventas.xlsx";
```

```text
ERROR SEM015 (semántico): LOAD solo admite archivos CSV (.csv); se recibió '.xlsx' en 'ventas.xlsx'.
```

SEM015 comprueba la extensión antes de intentar leer el archivo. Un problema
de lectura o estructura de un archivo con extensión `.csv` conserva SEM011.
