"""Símbolos y pila de ámbitos: global para datasets y local por tubería."""

from dataclasses import dataclass
from pathlib import Path
from .ast_nodes import Location
from .errors import SemanticError

DATASET = "DATASET"
NUMBER = "NUMBER"
STRING = "STRING"
BOOLEAN = "BOOLEAN"
NULL = "NULL"
UNKNOWN = "UNKNOWN"
ERROR = "ERROR"


@dataclass
class Symbol:
    """Registro básico con los mismos campos del ejemplo del profesor."""
    name: str
    type_: str
    scope: str
    line: int
    initialized: bool = False
    used: bool = False


@dataclass
class ColumnSymbol:
    name: str
    datatype: str
    nullable: bool = False
    scope: str = "global"
    line: int = 0
    initialized: bool = True
    used: bool = False

    @property
    def type_(self) -> str:
        return self.datatype


@dataclass
class DatasetSymbol:
    name: str
    path: Path
    location: Location
    columns: dict[str, ColumnSymbol] | None
    scope: str = "global"
    initialized: bool = False
    used: bool = False

    @property
    def type_(self) -> str:
        return DATASET

    @property
    def line(self) -> int:
        return self.location.line


SymbolRecord = Symbol | ColumnSymbol | DatasetSymbol


class SymbolTable:
    def __init__(self):
        # {nombre_de_ámbito: {nombre_de_identificador: símbolo}}
        self._table: dict[str, dict[str, SymbolRecord]] = {"global": {}}
        self._scope_stack: list[str] = ["global"]

    @property
    def current_scope(self) -> str:
        return self._scope_stack[-1]

    @property
    def current_symbols(self) -> dict[str, SymbolRecord]:
        return self._table[self.current_scope]

    @property
    def datasets(self) -> dict[str, DatasetSymbol]:
        """Vista compatible con la salida JSON y el driver anterior."""
        return {name: symbol for name, symbol in self._table["global"].items()
                if isinstance(symbol, DatasetSymbol)}

    @property
    def scopes(self) -> dict[str, dict[str, SymbolRecord]]:
        return self._table

    def enter_scope(self, name: str) -> None:
        self._scope_stack.append(name)
        self._table.setdefault(name, {})

    def exit_scope(self) -> None:
        if len(self._scope_stack) == 1:
            raise RuntimeError("No se puede salir del ámbito global.")
        self._scope_stack.pop()

    def declare(self, name: str, type_: str, line: int, *,
                symbol: SymbolRecord | None = None) -> SymbolRecord:
        """declare(nombre, tipo, línea), como en SymbolTable del ejemplo."""
        if name in self.current_symbols:
            raise SemanticError("SEM002",
                                f"'{name}' ya fue declarado en el ámbito '{self.current_scope}'.",
                                line)
        if symbol is None:
            symbol = Symbol(name, type_, self.current_scope, line)
        symbol.scope = self.current_scope
        self.current_symbols[name] = symbol
        return symbol

    def lookup(self, name: str) -> SymbolRecord | None:
        for scope in reversed(self._scope_stack):
            symbol = self._table[scope].get(name)
            if symbol is not None:
                return symbol
        return None

    def replace_columns(self, columns: dict[str, ColumnSymbol]) -> None:
        """GROUP_BY cambia las columnas visibles en la tubería actual."""
        if self.current_scope == "global":
            raise RuntimeError("Las columnas de una tubería necesitan un ámbito local.")
        # Copiar el mapa evita tratar un dict de columnas como un dict mutable
        # de cualquier símbolo. Los registros de columnas siguen compartidos.
        self._table[self.current_scope] = dict(columns)

    def unused_warnings(self) -> list[str]:
        return [f"ADVERTENCIA: '{symbol.name}' declarado en línea {symbol.line} "
                f"del ámbito '{symbol.scope}' nunca fue usado."
                for symbols in self._table.values() for symbol in symbols.values()
                if not symbol.used]
