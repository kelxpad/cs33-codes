from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Route:
    u: int
    v: int
    w: int
