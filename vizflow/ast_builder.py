
"""Visitor para las reglas reales de VizFlowParser.g4 del equipo."""

from decimal import Decimal
from typing import Any

from gen.VizFlowParser import VizFlowParser
from gen.VizFlowParserVisitor import VizFlowParserVisitor

from . import ast_nodes as ast
from .symbols import BOOLEAN, NULL, NUMBER, STRING


def location(token: Any) -> ast.Location:
    return ast.Location(token.line, token.column + 1)


def decode_string(text: str) -> str:
    """El lexer permite escapes generales: los desconocidos se conservan."""
    value = text[1:-1]

    escapes = {
        'n': '\n',
        'r': '\r',
        't': '\t',
        'b': '\b',
        'f': '\f',
        '"': '"',
        '\\': '\\',
        '/': '/'
    }

    output = []
    index = 0

    while index < len(value):
        char = value[index]

        if char == '\\' and index + 1 < len(value):
            following = value[index + 1]
            output.append(escapes.get(following, '\\' + following))
            index += 2
        else:
            output.append(char)
            index += 1

    return ''.join(output)


class ASTBuilder(VizFlowParserVisitor):
    # Los accesores de ANTLR son dinámicos.
    # El AST construido mantiene tipos explícitos.

    # ------------------------------------------------------------------------
    # 1. PROGRAMA Y SENTENCIAS
    # ------------------------------------------------------------------------

    def visitPrograma(self, ctx: Any) -> ast.Program:
        statements = [self.visit(ctx.sentencia())]

        statements.extend(
            self.visit(ctx.listaSentencias())
        )

        return ast.Program(
            location(ctx.start),
            statements
        )

    def visitListaSentencias(self, ctx: Any) -> list[ast.Node]:
        # Producción vacía: no existen más sentencias.
        if ctx.sentencia() is None:
            return []

        return [
            self.visit(ctx.sentencia()),
            *self.visit(ctx.listaSentencias())
        ]

    def visitSentencia(self, ctx: Any) -> ast.Node:
        return self.visit(ctx.getChild(0))

    # ------------------------------------------------------------------------
    # 2. DECLARACIÓN Y CARGA DE DATASETS
    # ------------------------------------------------------------------------

    def visitDeclaracionDataset(self, ctx: Any) -> ast.LoadDataset:
        return ast.LoadDataset(
            location(ctx.ID().symbol),
            ctx.ID().getText(),
            decode_string(ctx.STRING_LIT().getText())
        )

    # ------------------------------------------------------------------------
    # 3. PIPELINE GENERAL
    # ------------------------------------------------------------------------

    def visitPipeline(self, ctx: Any) -> ast.Pipeline:
        # Primera operación obligatoria.
        operations: list[ast.Node] = [
            self.visit(ctx.operacion())
        ]

        # Operaciones adicionales definidas mediante recursión.
        operations.extend(
            self.visit(ctx.operacionesAdicionales())
        )

        # DASHBOARD es opcional.
        dashboard = ctx.dashboardOpcional()

        if dashboard.DASHBOARD() is not None:
            operations.append(
                ast.Dashboard(
                    location(dashboard.DASHBOARD().symbol)
                )
            )

        return ast.Pipeline(
            location(ctx.ID().symbol),
            ctx.ID().getText(),
            operations
        )

    def visitOperacionesAdicionales(self, ctx: Any) -> list[ast.Node]:
        # Producción vacía: termina el pipeline.
        if ctx.operacion() is None:
            return []

        return [
            self.visit(ctx.operacion()),
            *self.visit(ctx.operacionesAdicionales())
        ]

    def visitOperacion(self, ctx: Any) -> ast.Node:
        return self.visit(ctx.getChild(0))

    # ------------------------------------------------------------------------
    # 4. OPERACIÓN FILTER
    # ------------------------------------------------------------------------

    def visitFilterOp(self, ctx: Any) -> ast.Filter:
        return ast.Filter(
            location(ctx.start),
            self.visit(ctx.expresionLogica())
        )

    # Precedencia lógica: NOT > AND > OR.

    def visitExpresionLogica(self, ctx: Any) -> ast.Node:
        left = self.visit(ctx.expresionAnd())

        return self._fold_continuation(
            left,
            ctx.continuacionOr(),
            'expresionAnd',
            'continuacionOr'
        )

    def visitExpresionAnd(self, ctx: Any) -> ast.Node:
        left = self.visit(ctx.expresionNot())

        return self._fold_continuation(
            left,
            ctx.continuacionAnd(),
            'expresionNot',
            'continuacionAnd'
        )

    def visitExpresionNot(self, ctx: Any) -> ast.Node:
        if ctx.NOT() is not None:
            return ast.Unary(
                location(ctx.NOT().symbol),
                'NOT',
                self.visit(ctx.expresionNot())
            )

        if ctx.comparacion() is not None:
            return self.visit(ctx.comparacion())

        return self.visit(ctx.expresionLogica())

    def visitComparacion(self, ctx: Any) -> ast.Binary:
        column = ast.Column(
            location(ctx.ID().symbol),
            ctx.ID().getText()
        )

        operator = ctx.operadorRelacional().start

        return ast.Binary(
            location(operator),
            operator.text,
            column,
            self.visit(ctx.valor())
        )

    def visitValor(self, ctx: Any) -> ast.Node:
        return self._value(ctx)

    # ------------------------------------------------------------------------
    # 5. OPERACIÓN TRANSFORM
    # ------------------------------------------------------------------------

    def visitTransformOp(self, ctx: Any) -> ast.Transform:
        return ast.Transform(
            location(ctx.ID().symbol),
            ctx.ID().getText(),
            self.visit(ctx.expresionAritmetica())
        )

    # Precedencia aritmética:
    # Paréntesis > multiplicación/división > suma/resta.

    def visitExpresionAritmetica(self, ctx: Any) -> ast.Node:
        left = self.visit(ctx.termino())

        return self._fold_continuation(
            left,
            ctx.continuacionSuma(),
            'termino',
            'continuacionSuma'
        )

    def visitTermino(self, ctx: Any) -> ast.Node:
        left = self.visit(ctx.factor())

        return self._fold_continuation(
            left,
            ctx.continuacionProducto(),
            'factor',
            'continuacionProducto'
        )

    def visitFactor(self, ctx: Any) -> ast.Node:
        if ctx.expresionAritmetica() is not None:
            return self.visit(ctx.expresionAritmetica())

        return self._value(ctx)

    # ------------------------------------------------------------------------
    # 6. OPERACIÓN GROUP_BY
    # ------------------------------------------------------------------------

    def visitGroupByOp(self, ctx: Any) -> ast.GroupBy:
        return ast.GroupBy(
            location(ctx.ID().symbol),
            ctx.ID().getText(),
            [self.visit(ctx.agregacion())]
        )

    def visitAgregacion(self, ctx: Any) -> ast.Aggregate:
        if ctx.COUNT() is not None:
            return ast.Aggregate(
                location(ctx.start),
                'COUNT',
                []
            )

        token = ctx.ID().symbol

        return ast.Aggregate(
            location(ctx.start),
            ctx.funcionAgregacion().getText(),
            [
                ast.Column(
                    location(token),
                    token.text
                )
            ]
        )

    # ------------------------------------------------------------------------
    # 7. OPERACIÓN PLOT
    # ------------------------------------------------------------------------

    def visitPlotOp(self, ctx: Any) -> ast.Plot:
        identifiers = ctx.ID()

        axes = [
            ast.Axis(
                location(ctx.X().symbol),
                'x',
                ast.Column(
                    location(identifiers[0].symbol),
                    identifiers[0].getText()
                )
            ),
            ast.Axis(
                location(ctx.Y().symbol),
                'y',
                ast.Column(
                    location(identifiers[1].symbol),
                    identifiers[1].getText()
                )
            )
        ]

        return ast.Plot(
            location(ctx.start),
            ctx.tipoGrafico().getText(),
            axes
        )

    # ------------------------------------------------------------------------
    # 8. CONSTRUCCIÓN DE EXPRESIONES BINARIAS
    # ------------------------------------------------------------------------

    def _fold_continuation(
        self,
        left: ast.Node,
        ctx: Any,
        operand_rule: str,
        continuation_rule: str
    ) -> ast.Node:
        """
        Recorre las continuaciones recursivas del parser y construye
        el AST respetando la asociatividad izquierda.

        Ejemplo:
            10 - 3 - 2  ->  (10 - 3) - 2
        """

        while ctx is not None:
            operand_ctx = getattr(ctx, operand_rule)()

            # Producción vacía: termina la expresión.
            if operand_ctx is None:
                break

            # El primer token corresponde al operador.
            operator = ctx.start

            # Construir el operando derecho.
            right = self.visit(operand_ctx)

            # Combinar el resultado acumulado con el nuevo operando.
            left = ast.Binary(
                location(operator),
                operator.text.upper(),
                left,
                right
            )

            # Continuar con la siguiente operación.
            ctx = getattr(ctx, continuation_rule)()

        return left

    # ------------------------------------------------------------------------
    # 9. CONVERSIÓN DE VALORES A NODOS DEL AST
    # ------------------------------------------------------------------------

    def _value(self, ctx: Any) -> ast.Node:
        kind = ctx.start.type
        text = ctx.start.text
        loc = location(ctx.start)

        if kind == VizFlowParser.ID:
            return ast.Column(loc, text)

        if kind in {
            VizFlowParser.INT_LIT,
            VizFlowParser.FLOAT_LIT
        }:
            return ast.Literal(
                loc,
                Decimal(text),
                NUMBER
            )

        if kind == VizFlowParser.STRING_LIT:
            return ast.Literal(
                loc,
                decode_string(text),
                STRING
            )

        if kind in {
            VizFlowParser.TRUE,
            VizFlowParser.FALSE
        }:
            return ast.Literal(
                loc,
                kind == VizFlowParser.TRUE,
                BOOLEAN
            )

        if kind == VizFlowParser.NULL:
            return ast.Literal(
                loc,
                None,
                NULL
            )

        raise TypeError(
            f'Token de valor no esperado: {text!r}'
        )

