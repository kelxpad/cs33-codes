class TreeNode:
    def __init__(self, v: int):
        self.val = v
        self.p = None
        self.children = []
        self.jumps = []
        self.depth = None
        super().__init__()

    def __repr__(self):
        return str(self.val)
    
    def set_jumps(self, n: int):
        # number of binary lifting levels allowed
        max_log = n.bit_length() # ceil(lg_2(n + 1))

        self.jumps = [None] * max_log

        self.jumps[0] = self.p # 2^0 ancestor

        # build higher ancestors
        for i in range(1, max_log):
            prev = self.jumps[i - 1]
            if prev is None:
                break
            self.jumps[i] = prev.jumps[i - 1]
        
        for c in self.children:
            c.set_jumps(n)

def edgelist_to_adj(n, el):
    adj = {i: [] for i in range(n)}
    for u, v in el:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def get_rooted_tree(adj, vals, root):
    node_objs = [None for _ in range(len(vals))]

    def _dfs(i, p):
        node = TreeNode(vals[i])
        node_objs[i] = node

        if p is None:
            node.p = node
            node.depth = -1
        else:
            node.p = p
        
        node.depth = node.p.depth + 1

        for j in adj[i]:
            if p is None or j != p.val:
                node.children.append(_dfs(j, node))
        
        return node
    
    root_node = _dfs(root, None)
    return root_node, node_objs

def lca(u: TreeNode, v: TreeNode) -> TreeNode:
    # ensure u has greater depth
    if u.depth < v.depth:
        u,v = v,u

    # lift deeper node up
    diff = u.depth - v.depth
    i = 0
    while diff:
        if diff & 1:
            u = u.jumps[i]
        diff >>= 1
        i += 1

    if u == v:
        return u
    
    # lift both nodes
    for i in reversed(range(len(u.jumps))):
        if u.jumps[i] != v.jumps[i]:
            u = u.jumps[i]
            v = v.jumps[i]
    
    return u.p
    

# ---------------- TEST ---------------- #

edgelist_G1 = (10, [
    (4, 1),
    (1, 5),
    (1, 0),
    (0, 3),
    (0, 2),
    (2, 6),
    (2, 7),
    (6, 8),
    (8, 9),
])

adj = edgelist_to_adj(*edgelist_G1)
n, el = edgelist_G1

tree, nodes = get_rooted_tree(adj, [i for i in range(n)], 0)
tree.set_jumps(n)

for i in range(len(nodes)):
    print(f'{i}: {nodes[i].jumps}')
    
print("LCA(9,7) =", lca(nodes[9], nodes[7]))
print("LCA(8,6) =", lca(nodes[8], nodes[6]))
print("LCA(3,5) =", lca(nodes[3], nodes[5]))
