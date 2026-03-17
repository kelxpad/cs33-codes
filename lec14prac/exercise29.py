# Exercise 29. Find an 𝒪︀(n**2) implementation of the Gale-Shapley algorithm. (And implement it!)
from collections import deque

class GaleShapley:
    def __init__(self, pref_l: list[list[int]], pref_r: list[list[int]]):
        """
        pref_l[i]: preference list of proposer i 
        pref_r[j]: preference list of receiver j
        """
        self.pref_l = pref_l
        self.pref_r = pref_r
        self.n = len(pref_l)

        # match_l[i] = j, match_r[j] = i
        self.match_l = [-1] * self.n
        self.match_r = [-1] * self.n

        # next proposal index for each proposer
        self.next = [0] * self.n

        # rank_r[j][i] = how much j prefers i (smaller = better)
        self.rank_r = [[0] * self.n for _ in range(self.n)]
        for j in range(self.n):
            for rank, i in enumerate(self.pref_r[j]):
                self.rank_r[j][i] = rank
    
    def solve(self) -> tuple[list[int], list[int]]:
        free = deque(range(self.n)) # all proposers start free

        while free:
            i = free.popleft()

            # next receiver to propose to
            j = self.pref_l[i][self.next[i]]
            self.next[i] += 1

            if self.match_r[j] == -1:
                #if j is free, then match immediately
                self.match_l[i] = j
                self.match_r[j] = i
            
            else:
                i2 = self.match_r[j]
                # j prefer i over current partner?
                if self.rank_r[j][i] < self.rank_r[j][i2]:
                    # j switches
                    self.match_l[i] = j
                    self.match_r[j] = i

                    self.match_l[i2] = -1
                    free.append(i2)
                else:
                    # j rejects i
                    free.append(i)
        
        return self.match_l, self.match_r


pref_l = [
    [0, 1, 2],
    [1, 0, 2],
    [1, 2, 0]
]

pref_r = [
    [1, 0, 2],
    [0, 1, 2],
    [0, 1, 2]
]

gs = GaleShapley(pref_l, pref_r)
match_l, match_r = gs.solve()

print(match_l)  # proposer → receiver
print(match_r)  # receiver → proposer