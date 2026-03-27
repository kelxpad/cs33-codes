"""
grid problem!!
"""
from collections.abc import Sequence

def immigrants_game(x: Sequence[Sequence[int]]) -> list[int]:
    r = len(x)
    c = len(x[0])

    def in_bounds(i, j): return 0 <= i < r and 0 <= j < c
