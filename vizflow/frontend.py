"""ANTLR -> árbol sintáctico -> AST -> análisis semántico."""

from dataclasses import dataclass
from pathlib import Path
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from gen.VizFlowLexer import VizFlowLexer
from gen.VizFlowParser import VizFlowParser
from .ast_nodes import Location, Program
from .diagnostics import Diagnostic
from .semantic import AnalysisResult
from .semantic_visitor import SemanticVisitor


class CollectErrors(ErrorListener):
    def __init__(self, phase: str, code: str):
        super().__init__()
        self.phase = phase
        self.code = code
        self.diagnostics = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.diagnostics.append(Diagnostic(self.code, msg, Location(line, column + 1), self.phase))


@dataclass
class FrontendResult:
    program: Program | None
    analysis: AnalysisResult | None
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not self.diagnostics


def analyze_source(source: str, base_dir: Path) -> FrontendResult:
    lexical_errors = CollectErrors("léxico", "LEX001")
    lexer = VizFlowLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexical_errors)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    for token in tokens.tokens:
        if token.type == VizFlowLexer.ERROR_CHAR:
            lexical_errors.diagnostics.append(Diagnostic(
                "LEX001", f"Carácter no reconocido {token.text!r}.",
                Location(token.line, token.column + 1), "léxico"))
    if lexical_errors.diagnostics:
        return FrontendResult(None, None, lexical_errors.diagnostics)
    syntax_errors = CollectErrors("sintáctico", "SYN001")
    parser = VizFlowParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(syntax_errors)
    tree = parser.programa()
    if syntax_errors.diagnostics:
        return FrontendResult(None, None, syntax_errors.diagnostics)
    visitor = SemanticVisitor(base_dir)
    analysis = visitor.visit(tree)
    return FrontendResult(visitor.program, analysis, analysis.diagnostics)
