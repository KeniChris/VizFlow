from dataclasses import dataclass
from .ast_nodes import Location


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    location: Location
    phase: str = "semántico"

    def render(self, filename: str) -> str:
        return (f"{filename}:{self.location.line}:{self.location.column}: "
                f"ERROR {self.code} ({self.phase}): {self.message}")
