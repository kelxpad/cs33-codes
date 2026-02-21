from collections.abc import Sequence
from monster import Move

def min_starting_mp(n: int, moves: Sequence[Move]) -> int | None:
    inf = float("inf")

    #  req[h] = minimum mp required when monster has health h
    req = [inf] * (n + 1)
    req[0] = 0

    # pre-group moves by required health
    by_health = [[] for _ in range(n + 1)]
    for mv in moves:
        if 0 <= mv.h <= n:
            by_health[mv.h].append(mv)

    # modified bellman-ford
    for _ in range(n + 1):
        updated = False
        for h in range(n + 1):
            # if no moves usable, skip iter
            if not by_health[h]: 
                continue
            # iterate over all outgoing edges
            for mv in by_health[h]:
                h2 = h - mv.d
                # clamp underflow/overflow
                if h2 < 0:
                    h2 = 0
                elif h2 > n:
                    h2 = n
                
                # mv.s to pay for move or 
                # mv.s + req[h2] so we can finish after paying
                need = max(mv.s, mv.s + req[h2])

                # relax for health h
                if need < req[h]:
                    req[h] = need
                    updated = True
        
        if not updated: # no changes
            break
    
    # no farming infinte MP
    for h in range(n + 1):
        if not by_health[h]:
            continue
        for mv in by_health[h]:
            h2 = h - mv.d
            if h2 < 0:
                h2 = 0
            elif h2 > n:
                h2 = n
            
            need = max(mv.s, mv.s + req[h2])
            if need < req[h]:
                return 0
            
    if req[n] == inf:
        return None
    
    # starting mp cannot be negative
    return max(0, req[n])