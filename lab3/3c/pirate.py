from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Route:
    p: int
    q: int
    d: int
