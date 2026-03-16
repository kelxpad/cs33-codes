from random import randint, seed, sample
from lab04dbrute import brute_investigations
from lab04d import max_investigations
from collections import defaultdict

def check_ans(n, roads, haunted, h, investigations):

    cap = defaultdict(int)
    for u,v,k in roads:
        cap[(u,v)] += k
        cap[(v,u)] += k

    used = defaultdict(int)

    for t,cycle in investigations:

        assert cycle[0] == h
        assert cycle[-1] == h


        for i in range(len(cycle)-1):
            u = cycle[i]
            v = cycle[i+1]

            used[(u,v)] += 1
            used[(v,u)] += 1

            assert used[(u,v)] <= cap[(u,v)]
            
seed(67)

for test in range(100000):
    n = randint(2,6)
    m = randint(1,8)
    roads = []
    for _ in range(m):
        u = randint(1,n)
        v = randint(1,n)
        if u == v:
            continue
        k = randint(1,2)
        roads.append((u,v,k))
    h = randint(1,n)
    candidates = [i for i in range(1, n+1) if i != h]
    haunted = sample(candidates, randint(1, min(3, len(candidates))))    
    try:
        print(f"n={n}, roads={roads}, haunted={haunted}, h={h}")
        ans1 = max_investigations(n, roads, haunted, h)
        ans2 = brute_investigations(n, roads, haunted, h)

        check_ans(n, roads, haunted, h, ans1)
        print(f"original={ans1}, brute={ans2}")

        if ans1 != ans2:
            print("Mismatch!")
            print(n, roads, haunted, h)
            print(f"original={ans1}, brute={ans2}")
            break

    except Exception as e:
        print("RTE FOUND")
        print(n, roads, haunted, h)
        raise

    print(f"Test #{test+1} done")