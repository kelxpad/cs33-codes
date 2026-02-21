from dataclasses import dataclass

@dataclass(frozen=True)
class Road:
    a: int
    b: int
    t: int
    c: int
