"""
lab theme: one piece
persistent bst with range sum query but
i lack the bandwidth to implement that so 
im just gonna do bruteforce while laying
down the foundation yesyes
"""
from dataclasses import dataclass
@dataclass (slots=True)
class Node:
    value: int
    l: "Node | None" = None
    r: "Node | None" = None
    height: int = 0
    subtree_sum: int = 0
    i: int = 0
    j: int = 0

class PersistentAVLTree:
    def __init__(self, ls: list[int]):
        self.versions = []
        root = None
        for item in ls:
            root = self.insert(item, root, True)
        self.versions.append(root)
        super().__init__()
    
    def _height(self, u: Node)->int:
        return -1 if u == None else u.height
    
    def _recalc_height(self, u:Node):
        u.height = max(self._height(u.l), self._height(u.r)) + 1

    def _subtree_sum(self, u: Node)->int:
        return 0 if u == None else u.subtree_sum
    
    def _recalc_subtree_sum(self, u:Node):
        u.subtree_sum = self._subtree_sum(u.l) + self._subtree_sum(u.r) + u.value
    
    def _get_min(self, u: Node):
        return float('inf') if u == None else u.i
    
    def _get_max(self, u: Node):
        return float('-inf') if u == None else u.j

    def _recalc_ij(self, u:Node):
        u.i = min(u.value, self._get_min(u.l))
        u.j = max(u.value, self._get_max(u.r))
    
    def _create_node(self, l: Node, x: Node, r: Node):
        ret = Node(x.value, l, r)
        self._recalc_height(ret)
        self._recalc_subtree_sum(ret)
        self._recalc_ij(ret)
        return ret

    def _right_rot(self, u: Node)-> Node:
        assert u != None
        assert u.l != None
        a, b, c, d, e = u.l.l, u.l, u.l.r, u, u.r
        ret = self._create_node(a, b , self._create_node(c, d, e))
        return ret
    
    def _left_rot(self, u: Node) -> Node:
        assert u != None
        assert u.r != None
        a, b, c, d, e = u.l, u, u.r.l, u.r, u.r.r
        ret = self._create_node(self._create_node(a, b, c), d, e)
        return ret

    def _rebalance(self, u: Node) -> Node:
        if u == None:
            return u
        if self._height(u.l) >= self._height(u.r) + 2:
            left = u.l
            if self._height(u.l.l) < self._height(u.l.r):
                left = self._left_rot(u.l)
            return self._right_rot(self._create_node(left, u, u.r))
        elif self._height(u.l) + 2 <= self._height(u.r):
            right = u.r
            if self._height(u.r.r) < self._height(u.r.l):
                right = self._right_rot(u.r)
            return self._left_rot(self._create_node(u.l, u, right))
        else:
            return u

    def search(self, u: Node, x: int):
        if u == None:
            return False
        
        if u.value == x:
            return True
        elif u.value > x:
            return self.search(u.l, x)
        else:
            assert u.value < x
            return self.search(u.r, x)

    def _bst_insert(self, u: Node, x: int):
        if u == None:
            return Node(x, None, None, 0, x, x, x)
        
        if u.value > x:
            return self._create_node(self.insert(x, u.l, True), u, u.r)
        elif u.value < x:
            return self._create_node(u.l, u, self.insert(x, u.r, True))
        else:
            assert u.value == x
            return u

    def insert(self, x: int, root: Node, will_ret: bool = False):
        if will_ret:
            new_tree = self._rebalance(self._bst_insert(root, x))
            return new_tree
        else:
            new_tree = self._rebalance(self._bst_insert(root, x))
            self.versions.append(new_tree)

    def _bst_delete_leftmost(self, u: Node) -> tuple[Node, Node | None]:
        # TODO: Properly make sure that the right subtree of the leftmost node is correctly handled
        # Insight: The right subtree of the leftmost node is still to the left of the second leftmost node
        # IMPORTANT: Decide whether rebalancing for every subtree is the right choice
        assert u != None
        if u.l == None:
            ret = self._create_node(None, u, None)
            subtree = None
            if u.r != None:
                subtree = self._create_node(u.r.l, u.r, u.r.r)
            return ret, self._rebalance(subtree)
        else:
            node, subtree = self._bst_delete_leftmost(u.l)
            return node, self._rebalance(self._create_node(subtree, u, u.r))
    
    def _bst_delete(self, u: Node, x: int):
        if u == None:
            return u
        if u.value > x:
            return self._create_node(self.delete(x, u.l, True), u, u.r)
        elif u.value < x:
            return self._create_node(u.l, u, self.delete(x, u.r,True))
        else:
            assert u.value == x
            # TODO: Verify Correctness
            if u.r != None:
                new_u, new_u_r = self._bst_delete_leftmost(u.r)
                new_u = self._create_node(u.l, new_u, new_u_r)
                return new_u
            else:
                return u.l

    def delete(self, x: int, u: Node, will_ret: bool = False):
        if will_ret:
            new_tree = self._rebalance(self._bst_delete(u, x))
            return new_tree
        else:
            new_tree = self._rebalance(self._bst_delete(u, x))
            self.versions.append(new_tree)
    
    def update(self, x: int, y:int, u: Node):
        raw = self.delete(x, u, True)
        new_tree = self.insert(y, raw, True)
        self.versions.append(new_tree)
    
    def sum_range(self, l: int, r: int, u: Node):
        if u == None:
            return 0
        if l <= u.i and u.j <= r:
            return self._subtree_sum(u)
        elif r < u.i or u.j < l:
            return 0
        else:
            return self.sum_range(l, r, u.l) + self.sum_range(l, r, u.r) + (u.value if l <= u.value <= r  else 0)

# d is valid
# take care of duplicate states
# use previous states to calculate sum of current state
# Insight: You can reuse other versions aside from the latest version
class PoneArchive:
    def __init__(self, n: int, a: set[int]) -> None:
        self.n = n
        a = list(a)
        self.pavl_tree = PersistentAVLTree(a)
        super().__init__()

    def insert_inscription(self, d: int, x: int) -> None:
        considered_ver = self.pavl_tree.versions[d]
        if self.pavl_tree.search(considered_ver, x):
            raise ValueError
        self.pavl_tree.insert(x, considered_ver)


    def remove_inscription(self, d: int, x: int) -> None:
        considered_ver = self.pavl_tree.versions[d]
        if not(self.pavl_tree.search(considered_ver, x)):
            raise ValueError
        self.pavl_tree.delete(x, considered_ver)

    def update_inscription(self, d: int, x: int, y: int) -> None:
        considered_ver = self.pavl_tree.versions[d]
        if (not self.pavl_tree.search(considered_ver, x)) or (self.pavl_tree.search(considered_ver, y)):
            raise ValueError
        self.pavl_tree.update(x, y, self.pavl_tree.versions[d])

    def sum_inscription(self, d: int, l: int, r: int) -> int:
        # note that r is included
        return self.pavl_tree.sum_range(l, r, self.pavl_tree.versions[d])


if __name__ == "__main__":

    archive = PoneArchive(5, {1, 3, 5, 7, 9})
    # Doc 0: {1, 3, 5, 7, 9}

    assert archive.sum_inscription(0, 1, 5) == 9, f"{archive.versions[0]}, {archive.sum_inscription(0,1,5)}"
    assert archive.sum_inscription(0, 2, 4) == 3

    archive.insert_inscription(0, 10)
    # Doc 1: {1, 3, 5, 7, 9, 10}

    assert archive.sum_inscription(0, 7, 20) == 16 
    assert archive.sum_inscription(1, 7, 20) == 26 


    archive.update_inscription(0, 5, 4)
    # Doc 2: {1, 3, 4, 7, 9}
    # print(archive.versions[2])
    assert archive.sum_inscription(0, 1, 7) == 16
    assert archive.sum_inscription(2, 1, 7) == 15, f"{archive.sum_inscription(2,1,7)}"

    # print(archive.versions[1])
    archive.remove_inscription(1, 3)
    # Doc 3: {1, 5, 7, 9}

    assert archive.sum_inscription(3, 1, 5) == 6

    assert archive.sum_inscription(0, 0, 999999) == 25
    # print(archive.versions)
