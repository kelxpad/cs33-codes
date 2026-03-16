from lab04c import min_lockdown_cost as i1
from cbrute import min_lockdown_cost as i2, check_ans
from random import randint, seed, sample
seed(67)

for test in range(100000):
    r = 5
    c = 5
    grid = [[randint(1, 5) for j in range(c)] for i in range(r)]
    coords = [(i, j) for i in range(r) for j in range(c)]
    hh = sample(coords, 4)
    hunters = hh[:2]
    house = hh[2:]
    a1, cuts = i1(grid, hunters, house)
    # a2 = i2(grid, hunters, house)
    # print(*grid, sep="\n")
    # print(f"{hunters=}, {house=}")
    # print(a1, cuts)
    check_ans(grid, r, c, hunters, house, a1, cuts)
    print(f"Test #{test + 1} done")