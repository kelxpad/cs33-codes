from dataclasses import dataclass

type Route = tuple[int, int]

@dataclass(slots=True)
class Movement:
    route_idx: int | None
    s: int
    t: int
