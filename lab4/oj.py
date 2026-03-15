from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Conduit:
    x: int
    y: int
    l: int
    u: int
