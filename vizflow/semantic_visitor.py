"""Visitor semántico de ANTLR adaptado del enfoque de MiniLang a VizFlow."""

from pathlib import Path
from typing import Any
from gen.VizFlowParserVisitor import VizFlowParserVisitor
from .ast_builder import ASTBuilder, location
from .ast_nodes import LoadDataset, Node, Pipeline, Program
from .errors import SemanticError
from .semantic import AnalysisResult, SemanticAnalyzer
from .symbols import SymbolTable


class SemanticVisitor(VizFlowParserVisitor):
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.builder = ASTBuilder()
        self.analyzer = SemanticAnalyzer(self.base_dir)
        self.program: Program | None = None

    @property
    def symtab(self) -> SymbolTable:
        return self.analyzer.symbols

    @property
    def errors(self) -> list[SemanticError]:
        return self.analyzer.errors

    def visitPrograma(self, ctx: Any) -> AnalysisResult:
        # Reiniciar permite reutilizar el visitor sin arrastrar símbolos o errores.
        self.analyzer = SemanticAnalyzer(self.base_dir)
        self.program = Program(location(ctx.start), [])
        for statement in ctx.sentencia():
            self.program.statements.append(self.visit(statement))
        return AnalysisResult(self.program, self.symtab, self.analyzer.diagnostics,
                              self.analyzer.pipelines)

    def visitSentencia(self, ctx: Any) -> Node:
        return self.visit(ctx.getChild(0))

    def visitDeclaracionDataset(self, ctx: Any) -> LoadDataset:
        node = self.builder.visitDeclaracionDataset(ctx)
        self.analyzer._load(node)
        return node

    def visitPipeline(self, ctx: Any) -> Pipeline:
        node = self.builder.visitPipeline(ctx)
        self.analyzer._pipeline(node)
        return node
