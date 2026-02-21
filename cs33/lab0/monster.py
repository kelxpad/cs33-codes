from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    h: int
    d: int
    s: int
