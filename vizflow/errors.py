"""Errores semánticos con ubicación, siguiendo el ejemplo de clase."""

from .ast_nodes import Location
from .diagnostics import Diagnostic


class SemanticError(Exception):
    def __init__(self, code: str, message: str, line: int = 0, column: int = 1):
        super().__init__(
            f"[Error semántico {code}, línea {line}, columna {column}] {message}")
        self.code = code
        self.message = message
        self.line = line
        self.column = column

    def diagnostic(self) -> Diagnostic:
        return Diagnostic(self.code, self.message, Location(self.line, self.column))
