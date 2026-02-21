from lab1d import territory_shifts
from bf_lab1d import bf_territory_shifts
from collections.abc import Sequence
import random

type Gate = tuple[int, int]

def tester(cases: int) -> None:
    random.seed(1) # i want reproducible

    max_n = 80
    max_edges = 160

    # test correctness of trappable_halls with bf_trappable_halls
    for case in range(cases):
        n = random.randint(2, max_n)

        gates: list[Gate] = []
        seen = set()

        m = random.randint(0, max_edges)
        for _ in range(m):
            u = random.randint(1, n)
            v = random.randint(1, n)
            # if u != v and (u, v) not in seen: # toggle parallel edges
            gates.append((u, v))
            seen.add((u, v))
        
        bf = bf_territory_shifts(n, gates)
        fast = territory_shifts(n, gates)

        print(f"Case {case}: n={n}, gates={gates}")
        if bf != fast:
            print(f"FAILED! Mismatch: bf={bf}, fast={fast} ")
            return None

    print("All tests passed!")
    return None

tester(50000)
