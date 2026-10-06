"""Tabla global de datasets y esquemas locales de columnas."""

from dataclasses import dataclass
from pathlib import Path
from .ast_nodes import Location

NUMBER = "NUMBER"
STRING = "STRING"
BOOLEAN = "BOOLEAN"
NULL = "NULL"
UNKNOWN = "UNKNOWN"
ERROR = "ERROR"


@dataclass(frozen=True)
class ColumnSymbol:
    name: str
    datatype: str
    nullable: bool = False


@dataclass
class DatasetSymbol:
    name: str
    path: Path
    location: Location
    columns: dict[str, ColumnSymbol] | None


class SymbolTable:
    def __init__(self):
        self.datasets: dict[str, DatasetSymbol] = {}

    def declare(self, symbol: DatasetSymbol) -> bool:
        if symbol.name in self.datasets:
            return False
        self.datasets[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> DatasetSymbol | None:
        return self.datasets.get(name)
