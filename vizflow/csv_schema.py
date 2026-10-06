"""Lee el esquema de un CSV local; no ejecuta FILTER ni calcula estadísticas."""

import csv
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from .symbols import BOOLEAN, NUMBER, STRING, UNKNOWN, ColumnSymbol

NUMERIC_TEXT = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def infer_cell(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    if value.lower() in {"true", "false"}:
        return BOOLEAN
    if NUMERIC_TEXT.fullmatch(value):
        try:
            if Decimal(value).is_finite():
                return NUMBER
        except InvalidOperation:
            pass
    return STRING


def read_schema(path: Path) -> dict[str, ColumnSymbol]:
    observed: dict[str, set[str]] = {}
    nullable: dict[str, bool] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("El CSV está vacío y no tiene encabezados.") from None
        if not header or any(not name.strip() for name in header):
            raise ValueError("El CSV tiene un encabezado vacío.")
        if len(set(header)) != len(header):
            raise ValueError("El CSV tiene nombres de columnas repetidos.")
        for name in header:
            observed[name] = set()
            nullable[name] = False
        for row in reader:
            if not row:  # Una línea completamente vacía se ignora.
                continue
            if len(row) != len(header):
                raise ValueError(f"La fila CSV {reader.line_num} tiene {len(row)} "
                                 f"campos; se esperaban {len(header)}.")
            for name, value in zip(header, row):
                datatype = infer_cell(value)
                if datatype is None:
                    nullable[name] = True
                else:
                    observed[name].add(datatype)
    columns = {}
    for name, types in observed.items():
        datatype = next(iter(types)) if len(types) == 1 else STRING if types else UNKNOWN
        columns[name] = ColumnSymbol(name, datatype, nullable[name])
    return columns
