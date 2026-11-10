# Validaciones semánticas demostrables desde archivos .vf

## Criterio aplicado al material del curso

El apartado 4 de [Análisis Semántico, AST y Tablas de Símbolos](https://drive.google.com/file/d/1ogcgATV3PQwufb0ahMVZZDaGWNvm2qrV/view?usp=drivesdk)
describe el análisis semántico sobre programas sintácticamente correctos.
En [Ejemplo1 (5).zip](https://drive.google.com/file/d/1fpOzKux2e1IOSnN-LRjfAJujB-S89Ngw/view?usp=drivesdk),
`main.py` lee un archivo mediante `FileStream`, ejecuta el lexer y el parser,
y visita el árbol con `SemanticVisitor` para comprobar los identificadores.

Para VizFlow se aplica ese flujo a los programas `.vf`: cada código SEM del
catálogo debe poder observarse desde un archivo fuente que supere léxico y sintaxis.
Las pruebas sobre un AST construido manualmente no sustituyen esa demostración.
Esta es la decisión de implementación adoptada para el proyecto a partir del material;
las guías no especifican los códigos SEM ni la extensión `.vf` de VizFlow.

## Catálogo vigente: 11 códigos

| Código | Validación | Resultado desde un `.vf` actual |
| --- | --- | --- |
| SEM001 | Dataset no declarado | SEM001 |
| SEM002 | Dataset declarado dos veces | SEM002 |
| SEM003 | Columna inexistente | SEM003 |
| SEM004 | Tipos incompatibles en expresiones y operaciones | SEM004 |
| SEM007 | SUM, AVG, MIN y MAX requieren columnas numéricas | SEM007 |
| SEM008 | División por cero constante | SEM008 |
| SEM009 | Ejes y tipos de los gráficos | Los tipos incorrectos producen SEM009; la forma de los ejes también la restringe el parser |
| SEM011 | CSV inexistente, ilegible o con estructura incorrecta | SEM011 |
| SEM012 | Colisión de nombres en el resultado de GROUP_BY | SEM012 |
| SEM014 | Uso de una columna sin inicialización válida | SEM014 después del error que impidió inicializarla |
| SEM015 | LOAD requiere una extensión .csv, sin distinguir mayúsculas | SEM015, con la extensión recibida y la ruta |

Se conservan los identificadores existentes; los códigos retirados no se reutilizan.

## Códigos retirados

| Código retirado | Restricción que ya comprueba el parser | Resultado actual |
| --- | --- | --- |
| SEM005 | FILTER exige una condición con comparación | FILTER(monto) produce SYN001 |
| SEM006 | SUM/AVG/MIN/MAX reciben una columna y COUNT no recibe argumentos | SUM() o COUNT(monto) producen SYN001 |
| SEM010 | DASHBOARD solo puede cerrar la tubería | Una operación posterior produce SYN001 |
| SEM013 | Las agregaciones solo están permitidas en GROUP_BY | TRANSFORM(total = SUM(monto)) produce SYN001 |

Se eliminaron sus emisiones del analizador semántico y las pruebas que los
activaban con AST manuales. Sus restricciones siguen cubiertas como sintaxis.
La gramática del equipo se conserva.

## Pruebas reproducibles

```bash
python3 run_tests.py
```

`tests/test_semantico/test_diagnostics.py` abre los 11 archivos `.vf` y comprueba
los códigos exactos, su fase y su ubicación. Además, ejecuta esos mismos archivos
mediante `main.py --semantico --json` y comprueba la salida real y el código de
terminación. Los casos que la gramática impide deben producir SYN001.

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
