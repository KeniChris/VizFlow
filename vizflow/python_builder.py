"""Generador de código Python a partir del AST de VizFlow."""

from decimal import Decimal

from . import ast_nodes as ast


class PythonCodeBuilder:

    def __init__(self):
        self.lines = []
        self.indent_level = 0
        self.dataframe_name = "df"
        self.plots = []
        self.plot_counters = {}
        self.operations = []
        self.main_variable = None

    def _indent(self):
        """Devuelve la indentación actual."""
        return "    " * self.indent_level

    def _emit(self, code):
        """Agrega una línea de código."""
        self.lines.append(self._indent() + code)

    # ==================================================
    # 1. GENERACIÓN DEL PROGRAMA
    # ==================================================

    def generate(self, program: ast.Program) -> str:
        """Genera código Python a partir de un programa VizFlow."""

        self.lines = []
        self.indent_level = 0
        self.dataframe_name = "df"
        self.plots = []
        self.plot_counters = {}
        self.operations = []
        self.main_variable = None

        self._emit("import pandas as pd")
        self._emit("")

        for statement in program.statements:
            self.visit(statement)

        return "\n".join(self.lines) + "\n"

    # ==================================================
    # 2. VISITAR NODOS DEL AST
    # ==================================================

    def visit(self, node: ast.Node):
        """Identifica el tipo de nodo y delega su generación."""

        if isinstance(node, ast.LoadDataset):
            return self.visit_load_dataset(node)

        if isinstance(node, ast.Pipeline):
            return self.visit_pipeline(node)

        if isinstance(node, ast.Filter):
            return self.visit_filter(node)

        if isinstance(node, ast.Transform):
            return self.visit_transform(node)

        if isinstance(node, ast.GroupBy):
            return self.visit_group_by(node)

        if isinstance(node, ast.Plot):
            return self.visit_plot(node)

        if isinstance(node, ast.Dashboard):
            return self.visit_dashboard(node)

        raise NotImplementedError(
            f"Generación todavía no implementada para: "
            f"{type(node).__name__}"
        )

    # ==================================================
    # 3. LOAD DATASET
    # ==================================================

    def visit_load_dataset(self, node: ast.LoadDataset):
        """Genera la carga de un archivo CSV."""

        self._emit(
            f"{node.name} = pd.read_csv({node.path!r})"
        )
        
        self.operations.append({
            "type": "LOAD",
            "description": f"Cargar dataset desde {node.path}"
        })

    # ==================================================
    # 4. PIPELINE
    # ==================================================

    def visit_pipeline(self, node: ast.Pipeline):
        """Genera las operaciones de un pipeline."""

        self.dataframe_name = node.dataset

        # Recorre secuencialmente todas las operaciones
        # almacenadas en el pipeline.
        for operation in node.operations:
            self.visit(operation)

    # ==================================================
    # 5. FILTER
    # ==================================================

    def visit_filter(self, node: ast.Filter):
        """Genera una operación FILTER."""

        condition = self.build_expression(node.condition)

        self._emit(
            f"{self.dataframe_name} = "
            f"{self.dataframe_name}[{condition}]"
        )
        self.operations.append({
        "type": "FILTER",
        "description": f"Filtrar registros donde {condition}"
    })

    # ==================================================
    # 6. TRANSFORM
    # ==================================================

    def visit_transform(self, node: ast.Transform):
        """Genera una operación TRANSFORM."""

        expression = self.build_expression(node.expression)
        
        if self.main_variable is None:
            self.main_variable = node.target

        self._emit(
            f"{self.dataframe_name}[{node.target!r}] = "
            f"{expression}"
        )
        
        self.operations.append({
            "type": "TRANSFORM",
            "description": (
                f"Asignar {expression} a la columna {node.target}"
            )
        })

    # ==================================================
    # 7. GROUP_BY
    # ==================================================

    def visit_group_by(self, node: ast.GroupBy):
        """Genera una operación GROUP_BY."""

        if len(node.aggregates) != 1:
            raise NotImplementedError(
                "GROUP_BY actualmente admite una agregación."
            )

        aggregate = node.aggregates[0]

        # --------------------------------------------------
        # COUNT()
        # --------------------------------------------------

        if aggregate.function == "COUNT":
            output_name = f"total_{self.dataframe_name}"
            self.main_variable = output_name

            self._emit(
                f"{self.dataframe_name} = "
                f"{self.dataframe_name}.groupby({node.column!r})"
                f".size().reset_index(name={output_name!r})"
            )

            self.operations.append({
                "type": "GROUP_BY",
                "description": (
                    f"Agrupar por {node.column} "
                    f"utilizando COUNT"
                )
            })

            return

        # --------------------------------------------------
        # SUM, AVG, MIN y MAX
        # --------------------------------------------------

        functions = {
            "SUM": "sum",
            "AVG": "mean",
            "MIN": "min",
            "MAX": "max"
        }

        function = functions.get(aggregate.function)

        if function is None:
            raise ValueError(
                f"Agregación no soportada: {aggregate.function}"
            )

        # Verifica que la agregación tenga exactamente
        # una columna como argumento.
        if (
            len(aggregate.arguments) != 1
            or not isinstance(aggregate.arguments[0], ast.Column)
        ):
            raise ValueError(
                "La agregación necesita una columna como argumento."
            )

        column = aggregate.arguments[0].name
        self.main_variable = column

        self._emit(
            f"{self.dataframe_name} = "
            f"{self.dataframe_name}.groupby("
            f"{node.column!r}, as_index=False)"
            f".agg(**{{{column!r}: ({column!r}, {function!r})}})"
        )
        
        self.operations.append({
            "type": "GROUP_BY",
            "description": (
                f"Agrupar por {node.column} "
                f"utilizando {aggregate.function}"
            )
        })

    # ==================================================
    # 8. PLOT
    # ==================================================

    def visit_plot(self, node: ast.Plot):
        """Genera una operación PLOT."""

        # Traduce los tipos de gráfico de VizFlow
        # a los tipos reconocidos por pandas.
        functions = {
            "BAR": "bar",
            "LINE": "line",
            "SCATTER": "scatter"
        }

        kind = functions.get(node.kind)

        if kind is None:
            raise NotImplementedError(
                f"Gráfico todavía no implementado: {node.kind}"
            )

        # Obtiene los nombres de las columnas
        # correspondientes a los ejes X e Y.
        x = node.axes[0].expression.name
        y = node.axes[1].expression.name
        
        self.main_variable = y

        # Configura matplotlib para generar imágenes
        # sin abrir ventanas gráficas.
        self._emit("import matplotlib")
        self._emit("matplotlib.use('Agg')")
        self._emit("import matplotlib.pyplot as plt")
        self._emit("")

        # Genera la visualización utilizando pandas.
        self._emit(
            f"{self.dataframe_name}.plot("
            f"kind={kind!r}, x={x!r}, y={y!r})"
        )

        # Ajusta el gráfico y lo guarda como imagen.
        self._emit("plt.tight_layout()")

        # Incrementa el contador del tipo de gráfico.
        self.plot_counters[kind] = (
        self.plot_counters.get(kind, 0) + 1
        )

        number = self.plot_counters[kind]

        filename = f"grafico_{kind}_{number}.png"

        self._emit(f"plt.savefig({filename!r})")
        self._emit("plt.close()")
        self.plots.append(filename)
        
        self.operations.append({
            "type": "PLOT",
            "description": f"Generar gráfico de tipo {node.kind}"
        })

    # ==================================================
    # 9. DASHBOARD
    # ==================================================

    def visit_dashboard(self, node: ast.Dashboard):
        """Genera la instrucción para construir el dashboard."""

        self._emit(
            "from vizflow.dashboard_builder "
            "import generate_dashboard"
        )

        self._emit("")

        self._emit(
            f"generate_dashboard("
            f"{self.dataframe_name}, "
            f"plots={self.plots!r}, "
            f"operations={self.operations!r},"
            f"main_variable={self.main_variable!r})"
        )

    # ==================================================
    # 10. GENERACIÓN DE EXPRESIONES
    # ==================================================

    def build_expression(self, node: ast.Node) -> str:
        """Traduce un nodo de expresión del AST a código Python."""

        if isinstance(node, ast.Literal):
            return self._literal(node)

        if isinstance(node, ast.Column):
            return self._column(node)

        if isinstance(node, ast.Unary):
            return self._unary(node)

        if isinstance(node, ast.Binary):
            return self._binary(node)

        raise TypeError(
            f"Expresión no soportada: {type(node).__name__}"
        )

    # ==================================================
    # 11. LITERALES
    # ==================================================

    def _literal(self, node: ast.Literal) -> str:
        """Traduce valores literales."""

        value = node.value

        if isinstance(value, Decimal):
            return str(value)

        return repr(value)

    # ==================================================
    # 12. COLUMNAS
    # ==================================================

    def _column(self, node: ast.Column) -> str:
        """Traduce una referencia a columna."""

        return f'{self.dataframe_name}[{node.name!r}]'

    # ==================================================
    # 13. OPERADORES UNARIOS
    # ==================================================

    def _unary(self, node: ast.Unary) -> str:
        """Traduce operaciones unarias."""

        operand = self.build_expression(node.operand)

        operators = {
            "NOT": "~",
            "-": "-",
            "+": "+"
        }

        operator = operators.get(node.operator)

        if operator is None:
            raise ValueError(
                f"Operador unario no soportado: {node.operator}"
            )

        return f"({operator}{operand})"

    # ==================================================
    # 14. OPERADORES BINARIOS
    # ==================================================

    def _binary(self, node: ast.Binary) -> str:
        """Traduce operaciones binarias."""

        left = self.build_expression(node.left)
        right = self.build_expression(node.right)

        operators = {
            "AND": "&",
            "OR": "|",
            "==": "==",
            "!=": "!=",
            "<": "<",
            ">": ">",
            "<=": "<=",
            ">=": ">=",
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/"
        }

        operator = operators.get(node.operator)

        if operator is None:
            raise ValueError(
                f"Operador binario no soportado: {node.operator}"
            )

        return f"({left} {operator} {right})"
