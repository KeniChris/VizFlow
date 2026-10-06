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
    escapes = {'n': '\n', 'r': '\r', 't': '\t', 'b': '\b', 'f': '\f',
               '"': '"', '\\': '\\', '/': '/'}
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
    # Los accesores de ANTLR son dinámicos (lista o elemento según el índice).
    # Any se limita a esta frontera; el AST construido tiene tipos explícitos.
    def visitPrograma(self, ctx: Any) -> ast.Program:
        return ast.Program(location(ctx.start), [self.visit(item) for item in ctx.sentencia()])

    def visitSentencia(self, ctx: Any) -> ast.Node:
        return self.visit(ctx.getChild(0))

    def visitDeclaracionDataset(self, ctx: Any) -> ast.LoadDataset:
        return ast.LoadDataset(location(ctx.ID().symbol), ctx.ID().getText(),
                               decode_string(ctx.STRING_LIT().getText()))

    def visitPipeline(self, ctx: Any) -> ast.Pipeline:
        operations: list[ast.Node] = [self.visit(item) for item in ctx.operacion()]
        if ctx.DASHBOARD() is not None:
            operations.append(ast.Dashboard(location(ctx.DASHBOARD().symbol)))
        return ast.Pipeline(location(ctx.ID().symbol), ctx.ID().getText(), operations)

    def visitOperacion(self, ctx: Any) -> ast.Node:
        return self.visit(ctx.getChild(0))

    def visitFilterOp(self, ctx: Any) -> ast.Filter:
        return ast.Filter(location(ctx.start), self.visit(ctx.expresionLogica()))

    def visitTransformOp(self, ctx: Any) -> ast.Transform:
        return ast.Transform(location(ctx.ID().symbol), ctx.ID().getText(),
                             self.visit(ctx.expresionAritmetica()))

    def visitGroupByOp(self, ctx: Any) -> ast.GroupBy:
        return ast.GroupBy(location(ctx.ID().symbol), ctx.ID().getText(),
                           [self.visit(ctx.agregacion())])

    def visitAgregacion(self, ctx: Any) -> ast.Aggregate:
        if ctx.COUNT() is not None:
            return ast.Aggregate(location(ctx.start), 'COUNT', [])
        token = ctx.ID().symbol
        return ast.Aggregate(location(ctx.start), ctx.funcionAgregacion().getText(),
                             [ast.Column(location(token), token.text)])

    def visitPlotOp(self, ctx: Any) -> ast.Plot:
        identifiers = ctx.ID()
        axes = [ast.Axis(location(ctx.X().symbol), 'x',
                         ast.Column(location(identifiers[0].symbol), identifiers[0].getText())),
                ast.Axis(location(ctx.Y().symbol), 'y',
                         ast.Column(location(identifiers[1].symbol), identifiers[1].getText()))]
        return ast.Plot(location(ctx.start), ctx.tipoGrafico().getText(), axes)

    def _fold(self, ctx: Any, child_rule: str) -> ast.Node:
        operands = getattr(ctx, child_rule)()
        result: ast.Node = self.visit(operands[0])
        for index, operand in enumerate(operands[1:], 1):
            operator = ctx.getChild(2 * index - 1).symbol
            result = ast.Binary(location(operator), operator.text.upper(), result,
                                self.visit(operand))
        return result

    def visitExpresionLogica(self, ctx: Any) -> ast.Node:
        return self._fold(ctx, 'expresionAnd')

    def visitExpresionAnd(self, ctx: Any) -> ast.Node:
        return self._fold(ctx, 'expresionNot')

    def visitExpresionNot(self, ctx: Any) -> ast.Node:
        if ctx.NOT() is not None:
            return ast.Unary(location(ctx.NOT().symbol), 'NOT', self.visit(ctx.expresionNot()))
        if ctx.comparacion() is not None:
            return self.visit(ctx.comparacion())
        return self.visit(ctx.expresionLogica())

    def visitComparacion(self, ctx: Any) -> ast.Binary:
        column = ast.Column(location(ctx.ID().symbol), ctx.ID().getText())
        operator = ctx.operadorRelacional().start
        return ast.Binary(location(operator), operator.text, column, self.visit(ctx.valor()))

    def visitValor(self, ctx: Any) -> ast.Node:
        return self._value(ctx)

    def visitExpresionAritmetica(self, ctx: Any) -> ast.Node:
        return self._fold(ctx, 'termino')

    def visitTermino(self, ctx: Any) -> ast.Node:
        return self._fold(ctx, 'factor')

    def visitFactor(self, ctx: Any) -> ast.Node:
        if ctx.expresionAritmetica() is not None:
            return self.visit(ctx.expresionAritmetica())
        return self._value(ctx)

    def _value(self, ctx: Any) -> ast.Node:
        kind = ctx.start.type
        text = ctx.start.text
        loc = location(ctx.start)
        if kind == VizFlowParser.ID:
            return ast.Column(loc, text)
        if kind in {VizFlowParser.INT_LIT, VizFlowParser.FLOAT_LIT}:
            return ast.Literal(loc, Decimal(text), NUMBER)
        if kind == VizFlowParser.STRING_LIT:
            return ast.Literal(loc, decode_string(text), STRING)
        if kind in {VizFlowParser.TRUE, VizFlowParser.FALSE}:
            return ast.Literal(loc, kind == VizFlowParser.TRUE, BOOLEAN)
        if kind == VizFlowParser.NULL:
            return ast.Literal(loc, None, NULL)
        raise TypeError(f'Token de valor no esperado: {text!r}')
