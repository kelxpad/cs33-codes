class Node:
    def __init__(self, label):
        self.label = label
        self.tv = 0
        self.ch = [] 
        self.anc = []
        self.depth = -1
        self.subsize = 1
        self.topmost = None

class PirateHierarchy:
    def __init__(self, n: int, superiors) -> None:
        self.n = n
        self.el = list(map(lambda e: (e[0]-1, e[1]-1), superiors)) 
        self.adj = self.make_adj()
        
        self.nods = [None for _ in range(self.n)]
        self.tree = self.build_tree()

        self.arri = [-1 for _ in range(self.n)]
        self.arr = self.flatten_tree()
        self.seg = [0 for _ in range(4*self.n)]
        self.lazy = [0 for _ in range(4*self.n)]
        super().__init__()
    
    def make_adj(self):
        adj = [[] for _ in range(self.n)]
        for u, v in self.el:
            adj[u].append(v)

        return adj
   
    def build_seg(self, nodi, s, e): # [)
        if e - s == 1: 
            self.seg[nodi] = self.arr[s] 

        m = (s+e)//2
        self.build_seg(2*nodi + 1, s, m)
        self.build_seg(2*nodi + 2, m, e) 
        # You only care about the children
    
    def pushdown(self, nodi):
        if self.lazy[nodi]:
            self.lazy[2*nodi + 1] += self.lazy[nodi] 
            self.lazy[2*nodi + 2] += self.lazy[nodi]
            self.seg[2*nodi + 1] += self.lazy[nodi]
            self.seg[2*nodi + 2] += self.lazy[nodi]
            self.lazy[nodi] = 0

    def update_treasure(self, nodi, l, r, s, e, t):
        if l <= s and e <= r:
            self.lazy[nodi] += t
            self.seg[nodi] += t 
            return

        if s >= r or e <= l: # WHY WHY WHY WHY WHY
            return

        m = (s+e)//2 
        self.pushdown(nodi)
        self.update_treasure(2*nodi + 1, l, r, s, m, t) 
        self.update_treasure(2*nodi + 2, l, r, m, e, t)

    def spread_plunder(self, a: int, b: int, t: int) -> None:
        noda, nodb = self.nods[a-1], self.nods[b-1]
        while noda.topmost is not nodb.topmost:
            if noda.topmost.depth > nodb.topmost.depth:
                l, r = self.arri[noda.topmost.label], self.arri[noda.label]
                self.update_treasure(0, l, r+1, 0, self.n, t)
                noda = noda.topmost.anc[0]
            else:
                l, r = self.arri[nodb.topmost.label], self.arri[nodb.label]
                self.update_treasure(0, l, r+1, 0, self.n, t)
                nodb = nodb.topmost.anc[0]

        l, r = sorted([self.arri[noda.label], self.arri[nodb.label]])
        self.update_treasure(0, l, r+1, 0, self.n, t)
        return

    def build_tree(self):
        visited = set()
        
        def _dfs(v, nodu):
            nodv = Node(v)
            visited.add(v)
            self.nods[v] = nodv
            if nodu:
                nodv.anc.append(nodu)
                nodv.depth = nodu.depth + 1
            else: 
                nodv.depth = 0

            subsize = 0
            max_size = 0
            for nv in self.adj[v]:
                if nv in visited: continue
                ch = _dfs(nv, nodv)  
                subsize += ch.subsize
                if ch.subsize > max_size:
                    if max_size == 0:
                        max_size = ch.subsize 
                        nodv.ch.append(ch)
                        continue

                    max_size = ch.subsize
                    temp = nodv.ch[0]
                    nodv.ch[0] = ch
                    nodv.ch.append(temp)
                else: nodv.ch.append(ch) 
            
            nodv.subsize += subsize
            return nodv
        
        return _dfs(0, None)
    
    def flatten_tree(self):
        time = 0 
        arr = []

        def _dfs(nodv, nodt):
            nonlocal time
            nodv.topmost = nodt 
            arr.append(nodv.tv)
            self.arri[nodv.label] = time
            time += 1
            
            if nodv.ch:
                _dfs(nodv.ch[0], nodt)
                for i in range(1, len(nodv.ch)): 
                    _dfs(nodv.ch[i], nodv.ch[i]) 

        _dfs(self.tree, self.tree)
        return arr
 
    def query(self, nodi, i, s, e):
        if e - s == 1:
            return self.seg[nodi]

        m = (s+e)//2 
        self.pushdown(nodi)
        if i < m:
            return self.query(2*nodi+1, i, s, m)
        
        return self.query(2*nodi+2, i, m, e)

    def get_richness(self, p: int) -> int:
        return self.query(0, self.arri[p-1], 0, self.n)

