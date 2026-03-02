# We can consider the islands to be nodes
# We can use centers to keep 'tabs' on islands of certain distance from it
# We can do arithmetic, relative to the center, to get k distance islands

# Specifics:
#   Modify Subtree computation to include:
#   A distance array containing nodes of a certain distance d from the centroid
#   The above has an extra field for sum of trek values to the centroid 

type Bridge = tuple[int, int]

class Archipelago:
    def __init__(self, h: list[int], bridges: list[Bridge]) -> None:
        self.n = len(h)
        self.h = h
        self.bridges = tuple(map(lambda bi: (bi[0]-1, bi[1]-1), bridges))
        self.adj = self.make_adj(self.bridges)
        self.cents, self.dists, self.treks, self.sub_cents = self.get_all(0)
        super().__init__()

    def make_adj(self, el: list[Bridge]):
        adj = [[] for _ in range(self.n)]
        for u, v in el:
            adj[u].append(v)
            adj[v].append(u)
        return adj

    def get_subsize(self, u: int, p: int, removed: set[int]):
        sz = 1
        for v in self.adj[u]:
            if v not in removed and v != p:
                sz += self.get_subsize(v, u, removed)
        return sz

    def get_cent(self, r: int, removed: set[int]):
        n = self.get_subsize(r, -1, removed)
        centroid = None

        def _dfs(u: int, p: int):
            nonlocal centroid
            szu = 1
            is_centroid = True

            for v in self.adj[u]:
                if v != p and v not in removed:
                    szv = _dfs(v, u)
                    szu += szv

                    if 2 * szv > n:
                        is_centroid = False

            if 2 * szu < n:
                is_centroid = False  # 2*(n - szu) > n
            if is_centroid:
                centroid = u

            return szu

        _dfs(r, -1)
        return centroid

    def get_dists(self, cent: int, removed: set[int]):
        dists = []

        def _dfs(u: int, p: int, d: int):
            dists.append((u, d))
            for v in self.adj[u]:
                if v not in removed and v != p:
                    _dfs(v, u, d + 1)

        _dfs(cent, -1, 0)
        return dists

    def get_trek_v(self, cent, removed):
        trek_v = []

        def _dfs(u: int, p: int, va: int):
            trek_v.append((u, va))
            for v in self.adj[u]:
                if v not in removed and v != p:
                    _dfs(v, u, max(va, self.h[v]))

        _dfs(cent, -1, self.h[cent])
        return trek_v

    def get_subtree(self, cent: int, removed: set[int]):
        subtrees = []

        def _dfs(u: int, p: int, st: int):
            subtrees.append((u, st))
            for v in self.adj[u]:
                if v not in removed and v != p:
                    _dfs(v, u, st)

        for u in self.adj[cent]:
            if u not in removed:
                _dfs(u, cent, u)

        return subtrees

    def get_all(self, u: int) -> tuple[
        list[int], # cents
        dict[int, tuple[dict[int, list[int]], dict[int, int]]], # dist_cents (what the fuck)
        dict[int, dict[int, int]], # trek_v_cents
        dict[int, dict[int, int]] # subtree_cents
        ]:
        removed = set()
        cents = []
        dist_cents = {}
        trek_v_cents = {}
        subtree_cents = {}

        def _get_all_cents(v: int) -> None:
            cent = self.get_cent(v, removed)
            # These functions hold through the same argument of recursive
            # centroid decomposition
            dists = self.get_dists(cent, removed)
            trek_v = self.get_trek_v(cent, removed)
            subs = self.get_subtree(cent, removed)  # To avoid double counting

            cents.append(cent)

            # store node->depth map for O(1) lookup
            dist_nodes = {}
            node_depth = {}

            for u, d in dists:
                node_depth[u] = d
                dist_nodes.setdefault(d, []).append(u)

            dist_cents[cent] = (dist_nodes, node_depth)

            trek_nodes = {}
            for u, va in trek_v:
                trek_nodes[u] = va
            trek_v_cents[cent] = trek_nodes

            sub_nodes = {}
            for u, st in subs:
                sub_nodes[u] = st
            subtree_cents[cent] = sub_nodes

            removed.add(cent)
            for nv in self.adj[cent]:
                if nv not in removed:
                    _get_all_cents(nv)

        _get_all_cents(u)
        return cents, dist_cents, trek_v_cents, subtree_cents

    # changed sum_pairs to sum_value_lists inspired by mergesort and prefix sums for correct max-pair sum
    def sum_value_lists(self, a: int, b: int) -> int:
        if not a or not b:
            return 0

        a = sorted(a)
        b = sorted(b)

        na = len(a)
        nb = len(b)

        # prefix sums of a
        prefix_a = [0] * (na + 1)
        for i in range(na):
            prefix_a[i + 1] = prefix_a[i] + a[i]

        total = 0
        j = 0

        # first term: sum a * (b <= a)
        for i in range(na):
            while j < nb and b[j] <= a[i]:
                j += 1
            total += a[i] * j

        # second term: sum b * (a < b)
        i = 0
        for j in range(nb):
            while i < na and a[i] < b[j]:
                i += 1
            total += b[j] * i

        return total

    def get_archipelago_value(self, k: int) -> int:
        k -= 1
        if k == 0:
            return sum(self.h)

        total_answer = 0

        for c in self.cents:
            # unpack node_depth for faster lookup
            depth_map, node_depth = self.dists[c]
            trek_map = self.treks[c]
            subtree_map = self.sub_cents[c]

            # group nodes by subtree
            subtree_nodes = {}
            for node, st in subtree_map.items():
                subtree_nodes.setdefault(st, []).append(node)

            # global structure: depth -> sorted trek values
            global_depth = {}

            # include centroid itself
            global_depth[0] = [trek_map[c]]

            for st, nodes in subtree_nodes.items():
                local_depth = {}

                # collect subtree nodes by depth instead of scanning lists
                for u in nodes:
                    d = node_depth[u]
                    if d is None:
                        continue

                    local_depth.setdefault(d, []).append(trek_map[u])

                # count contribution between this subtree and global
                for d, vals in local_depth.items():
                    need = k - d
                    if need in global_depth:
                        total_answer += 2 * self.sum_value_lists(vals, global_depth[need])

                # merge local into global
                for d, vals in local_depth.items():
                    global_depth.setdefault(d, []).extend(vals)

        return total_answer
    
if __name__ == "__main__":
    arch = Archipelago(
    (10, 15, 20, 50),
    (
        (1, 2),
        (3, 2),
        (4, 2),
    ),
)

    assert arch.get_archipelago_value(1) == 95
    assert arch.get_archipelago_value(2) == 170, f"got {arch.get_archipelago_value(2)}"
    assert arch.get_archipelago_value(3) == 240
    assert arch.get_archipelago_value(4) == 0