"""AST: conserva operaciones y operandos, no la puntuación de la gramática."""

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Location:
    line: int
    column: int


@dataclass
class Node:
    location: Location
    # Atributo sintetizado: lo completa el analizador en las expresiones.
    inferred_type: str | None = field(default=None, init=False, repr=False)


@dataclass
class Program(Node):
    statements: list[Node]


@dataclass
class LoadDataset(Node):
    name: str
    path: str


@dataclass
class Pipeline(Node):
    dataset: str
    operations: list[Node]


@dataclass
class Filter(Node):
    condition: Node


@dataclass
class Transform(Node):
    target: str
    expression: Node


@dataclass
class GroupBy(Node):
    column: str
    aggregates: list["Aggregate"]


@dataclass
class Axis(Node):
    name: str
    expression: Node


@dataclass
class Plot(Node):
    kind: str
    axes: list[Axis]


@dataclass
class Dashboard(Node):
    pass


@dataclass
class Literal(Node):
    value: Decimal | str | bool | None
    datatype: str


@dataclass
class Column(Node):
    name: str


@dataclass
class Unary(Node):
    operator: str
    operand: Node


@dataclass
class Binary(Node):
    operator: str
    left: Node
    right: Node


@dataclass
class Aggregate(Node):
    function: str
    arguments: list[Node]
