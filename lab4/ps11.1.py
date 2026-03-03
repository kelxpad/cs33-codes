# extended min cut problem: consider nodes/edges with capacities/costs in both

from collections import deque
from dataclasses import dataclass

class FlowNetwork: # edmonds-karp
    def __init__(self):
        self.graph: dict[str, dict[str, int]] = {}

    def add_edge(self, u: str, v: str, capacity: int) -> None:
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = capacity
        self.graph[v].setdefault(u, 0) # residual edge

    def bfs(self, source: str, sink: str, parent: dict[str, str]) -> int:
        visited = set([source])
        q = deque([(source, float("inf"))])

        while q:
            u, flow = q.popleft()
            for v, capacity in self.graph[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent[v] = u
                    new_flow = min(flow, capacity)
                    if v == sink:
                        return new_flow
                    q.append((v, new_flow))
        
        return 0
    
    def max_flow(self, source: str, sink: str) -> int:
        total_flow = 0

        while True:
            parent = {}
            flow = self.bfs(source, sink, parent)
            if flow == 0:
                break

            total_flow += flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= flow
                self.graph[v][u] += flow
                v = u

        return total_flow

@dataclass
class ExtendedGraph:
    nodes: list[str]
    edges: list[tuple[str, str, int]] # (u, v, edge_capacity)
    node_caps: dict[str, int] # node_capacity
    source: str
    sink: str

def transform_to_flow_network(ext: ExtendedGraph) -> tuple[FlowNetwork, str, str]:
    """
    performs node-splitting transformation:
    
    For each node i:
        i_entry -> i_exit with capacity = node_caps[i]
        
    for each edge (u -> v):
        u_exit -> v_entry with capacity = edge_capacity
    """

    fn = FlowNetwork()

    for node in ext.nodes:
        entry = f"{node}_in"
        exit = f"{node}_out"

        # node capacity edge
        cap = ext.node_caps.get(node, float("inf"))
        fn.add_edge(entry, exit, cap)

    for u, v, cap in ext.edges:
        fn.add_edge(f"{u}_out", f"{v}_in", cap)
    
    source = f"{ext.source}_in"
    sink = f"{ext.sink}_out"

    return fn, source, sink

# solver for extended min cut
def extended_min_cut(ext: ExtendedGraph) ->int:
    fn, source, sink = transform_to_flow_network(ext)
    return fn.max_flow(source, sink)

if __name__ == "__main__":
    ext_graph = ExtendedGraph(
        nodes=["s", "a", "b", "t"],
        edges=[
            ("s", "a", 3),
            ("a", "b", 2),
            ("b", "t", 4),
        ],
        node_caps={
            "s": float("inf"),
            "a": 5,
            "b": 3,
            "t": float("inf"),
        },
        source="s",
        sink="t",
    )

    result = extended_min_cut(ext_graph)
    print("Minimum cut cost:", result)