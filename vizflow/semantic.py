"""Comprobación estática sobre AST y tabla de símbolos; no depende de ANTLR."""

import csv
from dataclasses import dataclass, field
from decimal import DecimalException, Inexact, localcontext
from pathlib import Path
from . import ast_nodes as ast
from .csv_schema import read_schema
from .diagnostics import Diagnostic
from .symbols import (
    BOOLEAN, ERROR, NULL, NUMBER, STRING, UNKNOWN,
    ColumnSymbol, DatasetSymbol, SymbolTable,
)


@dataclass
class ExpressionInfo:
    datatype: str
    # Solo constantes del programa; no se evalúan las filas del CSV.
    constant: object = None


@dataclass
class PipelineSummary:
    dataset: str
    location: ast.Location
    columns: dict[str, ColumnSymbol]


@dataclass
class AnalysisResult:
    program: ast.Program
    symbols: SymbolTable
    diagnostics: list[Diagnostic] = field(default_factory=list)
    pipelines: list[PipelineSummary] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.diagnostics


class SemanticAnalyzer:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.symbols = SymbolTable()
        self.diagnostics: list[Diagnostic] = []
        self.pipelines: list[PipelineSummary] = []

    def error(self, code: str, node: ast.Node, message: str):
        self.diagnostics.append(Diagnostic(code, message, node.location))

    def analyze(self, program: ast.Program) -> AnalysisResult:
        self.symbols = SymbolTable()
        self.diagnostics = []
        self.pipelines = []
        for statement in program.statements:
            if isinstance(statement, ast.LoadDataset):
                self._load(statement)
            elif isinstance(statement, ast.Pipeline):
                self._pipeline(statement)
        return AnalysisResult(program, self.symbols, self.diagnostics, self.pipelines)

    def _load(self, node: ast.LoadDataset):
        original = self.symbols.lookup(node.name)
        if original is not None:
            self.error("SEM002", node, f"El dataset '{node.name}' ya fue declarado "
                       f"en la línea {original.location.line}.")
            return
        path = Path(node.path)
        if not path.is_absolute():
            path = self.base_dir / path
        try:
            path = path.resolve()
            columns = read_schema(path)
        except (OSError, UnicodeError, csv.Error, ValueError) as exc:
            self.error("SEM011", node, f"No se pudo obtener el esquema de '{node.path}': {exc}")
            columns = None
        # Evita falsos "no declarado" si ya se notificó un fallo del LOAD.
        self.symbols.declare(DatasetSymbol(node.name, path, node.location, columns))

    def _pipeline(self, node: ast.Pipeline):
        dataset = self.symbols.lookup(node.dataset)
        if dataset is None:
            self.error("SEM001", node, f"El dataset '{node.dataset}' no ha sido declarado.")
            return
        if dataset.columns is None:
            return
        # Entorno local: no se modifica el esquema del dataset fuente.
        schema = dict(dataset.columns)
        dashboard = False
        for operation in node.operations:
            if dashboard:
                self.error("SEM010", operation, "DASHBOARD debe ser la última operación.")
                continue
            if isinstance(operation, ast.Filter):
                info = self.infer(operation.condition, schema)
                if info.datatype not in {BOOLEAN, ERROR}:
                    self.error("SEM005", operation.condition,
                               f"FILTER necesita BOOLEAN; recibió {info.datatype}.")
            elif isinstance(operation, ast.Transform):
                info = self.infer(operation.expression, schema)
                if info.datatype not in {NUMBER, ERROR}:
                    self.error("SEM004", operation.expression,
                               f"TRANSFORM es aritmético y necesita NUMBER; recibió {info.datatype}.")
                    info = ExpressionInfo(ERROR)
                schema[operation.target] = ColumnSymbol(operation.target, info.datatype)
            elif isinstance(operation, ast.GroupBy):
                schema = self._group(operation, schema, node.dataset)
            elif isinstance(operation, ast.Plot):
                self._plot(operation, schema)
            elif isinstance(operation, ast.Dashboard):
                dashboard = True
        self.pipelines.append(PipelineSummary(node.dataset, node.location, dict(schema)))

    def _group(self, node: ast.GroupBy, schema: dict[str, ColumnSymbol], dataset_name: str):
        key = schema.get(node.column)
        if key is None:
            self.error("SEM003", node, f"La columna de agrupamiento '{node.column}' no existe.")
            key = ColumnSymbol(node.column, ERROR)
        output = {node.column: key}
        for call in node.aggregates:
            info = self.infer(call, schema, aggregate_context="group")
            argument = call.arguments[0] if len(call.arguments) == 1 else None
            # El DOCX usa SUM(monto) y después y=monto: se conserva ese nombre.
            # El avance del equipo usa COUNT() y luego y=total_clientes.
            name = f"total_{dataset_name}" if call.function == "COUNT" else (
                argument.name if isinstance(argument, ast.Column) else call.function.lower())
            if name in output:
                self.error("SEM012", call, f"GROUP_BY produciría dos columnas llamadas '{name}'. "
                           "La sintaxis actual no incluye alias; revisa los nombres de entrada.")
                continue
            output[name] = ColumnSymbol(name, info.datatype)
        return output

    def _plot(self, node: ast.Plot, schema):
        axes = {}
        for axis in node.axes:
            if axis.name not in {"x", "y"}:
                self.error("SEM009", axis, f"El eje '{axis.name}' no es válido; usa x o y.")
                continue
            if axis.name in axes:
                self.error("SEM009", axis, f"El eje '{axis.name}' está repetido.")
                continue
            axes[axis.name] = axis
        missing = {"x", "y"} - axes.keys()
        if missing:
            self.error("SEM009", node, "PLOT necesita los ejes: " + ", ".join(sorted(missing)) + ".")
        for name, axis in axes.items():
            value = axis.expression
            valid_form = isinstance(value, ast.Column)
            if not valid_form:
                self.error("SEM009", value,
                           "PLOT necesita nombres de columnas en ambos ejes.")
                continue
            info = self.infer(value, schema)
            if info.datatype == ERROR:
                continue
            if (name == "y" or node.kind == "SCATTER") and info.datatype != NUMBER:
                self.error("SEM009", value,
                           f"{node.kind}: el eje {name} necesita NUMBER; recibió {info.datatype}.")
            elif name == "x" and node.kind == "LINE" and info.datatype not in {NUMBER, STRING}:
                self.error("SEM009", value, "LINE: x necesita NUMBER o STRING.")

    @staticmethod
    def _typed(node: ast.Node, datatype: str, constant=None) -> ExpressionInfo:
        node.inferred_type = datatype
        return ExpressionInfo(datatype, constant)

    def infer(self, node: ast.Node, schema: dict[str, ColumnSymbol],
              aggregate_context: str | None = None, allow_unknown=False) -> ExpressionInfo:
        """El esquema es contexto heredado; el tipo es un atributo sintetizado."""
        if isinstance(node, ast.Literal):
            return self._typed(node, node.datatype, node.value)
        if isinstance(node, ast.Column):
            symbol = schema.get(node.name)
            if symbol is None:
                self.error("SEM003", node, f"La columna '{node.name}' no existe en este punto. "
                           "Disponibles: " + ", ".join(schema) + ".")
                return self._typed(node, ERROR)
            if symbol.datatype == UNKNOWN and not allow_unknown:
                self.error("SEM004", node, f"No se puede determinar el tipo de '{node.name}': "
                           "su CSV no contiene valores no vacíos para esa columna.")
                return self._typed(node, ERROR)
            return self._typed(node, symbol.datatype)
        if isinstance(node, ast.Aggregate):
            return self._aggregate(node, schema, aggregate_context)
        if isinstance(node, ast.Unary):
            info = self.infer(node.operand, schema, aggregate_context)
            expected = BOOLEAN if node.operator == "NOT" else NUMBER
            if info.datatype == ERROR:
                return self._typed(node, ERROR)
            if info.datatype != expected:
                self.error("SEM004", node, f"'{node.operator}' necesita {expected}; recibió {info.datatype}.")
                return self._typed(node, ERROR)
            constant = None
            if info.constant is not None:
                constant = (not info.constant if node.operator == "NOT"
                            else -info.constant if node.operator == "-" else info.constant)
            return self._typed(node, expected, constant)
        if isinstance(node, ast.Binary):
            op = node.operator
            # Una columna sin muestras tipadas sí puede comprobarse contra NULL.
            null_check = op in {"==", "!="} and any(
                isinstance(child, ast.Literal) and child.datatype == NULL
                for child in (node.left, node.right))
            left = self.infer(node.left, schema, aggregate_context, allow_unknown=null_check)
            right = self.infer(node.right, schema, aggregate_context, allow_unknown=null_check)
            if ERROR in {left.datatype, right.datatype}:
                return self._typed(node, ERROR)
            if op in {"+", "-", "*", "/"}:
                if left.datatype != NUMBER or right.datatype != NUMBER:
                    self.error("SEM004", node, f"'{op}' necesita NUMBER y NUMBER; recibió "
                               f"{left.datatype} y {right.datatype}.")
                    return self._typed(node, ERROR)
                if op == "/" and right.constant == 0:
                    self.error("SEM008", node.right, "División entre cero constante, conocida "
                               "durante el análisis semántico.")
                    return self._typed(node, ERROR)
                constant = None
                if left.constant is not None and right.constant is not None:
                    try:
                        with localcontext() as context:
                            context.prec = max(context.prec, 64)
                            context.traps[Inexact] = True
                            if op == "+":
                                constant = left.constant + right.constant
                            elif op == "-":
                                constant = left.constant - right.constant
                            elif op == "*":
                                constant = left.constant * right.constant
                            else:
                                constant = left.constant / right.constant
                    except DecimalException:
                        # No convertir redondeos en falsos ceros del programa.
                        pass
                return self._typed(node, NUMBER, constant)
            if op in {"AND", "OR"}:
                if left.datatype != BOOLEAN or right.datatype != BOOLEAN:
                    self.error("SEM004", node, f"{op} necesita BOOLEAN y BOOLEAN.")
                    return self._typed(node, ERROR)
                return self._typed(node, BOOLEAN)
            equality = op in {"==", "!="}
            if NULL in {left.datatype, right.datatype}:
                if equality:
                    return self._typed(node, BOOLEAN)
                self.error("SEM004", node, "NULL solo puede compararse con == o !=.")
                return self._typed(node, ERROR)
            compatible = left.datatype == right.datatype and (
                equality or left.datatype in {NUMBER, STRING})
            if not compatible:
                self.error("SEM004", node, f"No se puede comparar {left.datatype} con "
                           f"{right.datatype} usando '{op}'.")
                return self._typed(node, ERROR)
            return self._typed(node, BOOLEAN)
        raise TypeError(f"Nodo de expresión desconocido: {type(node).__name__}")

    def _aggregate(self, node: ast.Aggregate, schema, context):
        if context != "group":
            self.error("SEM013", node, "Las agregaciones se usan en GROUP_BY.")
            return self._typed(node, ERROR)
        argc = len(node.arguments)
        valid_arity = argc == 0 if node.function == "COUNT" else argc == 1
        if not valid_arity:
            expected = "cero argumentos" if node.function == "COUNT" else "un argumento"
            self.error("SEM006", node, f"{node.function} necesita {expected}; recibió {argc}.")
            return self._typed(node, ERROR)
        if argc and not isinstance(node.arguments[0], ast.Column):
            self.error("SEM006", node.arguments[0], "La agregación necesita el nombre de "
                       "una columna como argumento.")
            return self._typed(node, ERROR)
        if argc:
            info = self.infer(node.arguments[0], schema)
            if info.datatype == ERROR:
                return self._typed(node, ERROR)
            if node.function != "COUNT" and info.datatype != NUMBER:
                self.error("SEM007", node, f"{node.function} necesita una columna NUMBER; "
                           f"'{node.arguments[0].name}' es {info.datatype}.")
                return self._typed(node, ERROR)
        return self._typed(node, NUMBER)
