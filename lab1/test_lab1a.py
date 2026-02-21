from collections.abc import Sequence
from lab1a import trappable_halls
from bf_lab1a import bf_trappable_halls
type Hall = tuple[int, int]

import random
def tester(cases: int) -> None:
    random.seed(0) # i want reproducible

    max_n = 80
    max_extra_edges = 160
    # test correctness of trappable_halls with bf_trappable_halls
    for case in range(cases):
        nodes = random.randint(2, max_n)

        # build random spanning tree first to guarantee connectivity
        halls = []
        for v in range(2, nodes + 1):
            u = random.randint(1, v - 1)
            halls.append((u, v))

        # add extra random edges
        extra = random.randint(0, max_extra_edges)
        seen = set(halls) # prevent parallel edges
        for _ in range(extra):
            u = random.randint(1, nodes)
            v = random.randint(1, nodes)
            if u != v:
                a, b = min(u, v), max(u, v)
                if (a, b) not in seen:
                    halls.append((a, b))
                    seen.add((a, b))
        
        bf = bf_trappable_halls(nodes, halls)
        fast = trappable_halls(nodes, halls)

        print(f"Case {case}: n={nodes}, halls={halls}")
        if bf != fast:
            print(f"FAILED! Mismatch: bf={bf}, fast={fast} ")
            break

    print("All tests passed!")


tester(5000)

