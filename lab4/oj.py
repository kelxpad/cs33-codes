from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Conduit:
    x: int
    y: int
    l: int
    u: int

@dataclass(slots=True, frozen=True)
class Route:
    x: int  # station x
    y: int  # station y
    d: int  # current defense level
    e: int  # effectiveness value of fortifying this route