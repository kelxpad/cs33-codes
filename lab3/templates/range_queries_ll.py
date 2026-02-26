class Node:
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

class LinkedRangeQuery:
    def __init__(self, data: list, op: callable, identity) -> None:
        self.n = len(data)
        self.op = op
        self.identity = identity
        self.root = self.build(data, 0, self.n)

    def build(self, data: list, l: int, r: int) -> None:
        if r - l == 1:
            # leaf
            return Node(None, None, data[l])
        
        mid = (l + r) // 2
        left_child = self.build(data, l, mid)
        right_child = self.build(data, mid, r)

        value = self.op(left_child.value, right_child.value)
        return Node(left_child, right_child, value)
    
    def update(self, index: int, value) -> None:
        self._update(self.root, 0, self.n, index, value)

    def _update(self, node: Node, l: int, r: int, index: int, value) -> None:
        if r - l == 1:
            node.value = value
            return
        
        mid = (l + r) // 2
        if index < mid:
            self._update(node.left, l, mid, index, value)
        else:
            self._update(node.right, mid, r, index, value)

        # recompute current node after child update
        node.value = self.op(node.left.value, node.right.value)

    def range_query(self, left: int, right: int):
        return self._query(self.root, 0, self.n, left, right)
    
    def _query(self, node: Node, l: int, r: int, ql: int, qr: int):
        if qr <= l or r <= ql: # disjoint
            return self.identity
        
        if ql <= l and r <= qr: # in range
            return node.value
        
        mid = (l + r) // 2
        left_val = self._query(node.left, l, mid, ql, qr)
        right_val = self._query(node.right, mid, r, ql, qr)

        return self.op(left_val, right_val)
    
if __name__ == "__main__":

    # test sums
    arr = [1, 3, 5, 7, 9]
    rq = LinkedRangeQuery(arr, op=lambda a, b: a + b, identity=0)

    assert rq.range_query(0, 5) == sum(arr)
    assert rq.range_query(1, 4) == 3 + 5 + 7
    assert rq.range_query(2, 3) == 5
    assert rq.range_query(0, 0) == 0  # empty range

    rq.update(2, 10)  # change 5 -> 10
    arr[2] = 10

    assert rq.range_query(0, 5) == sum(arr), f"{rq.range_query(0, 5)}, {sum(arr)}"
    assert rq.range_query(1, 4) == 3 + 10 + 7


    # min tests
    arr = [5, 2, 8, 6, 1]
    rq = LinkedRangeQuery(arr, op=min, identity=float("inf"))

    assert rq.range_query(0, 5) == 1
    assert rq.range_query(1, 4) == 2
    assert rq.range_query(4, 5) == 1

    rq.update(4, 100)
    assert rq.range_query(0, 5) == 2


    # max tests
    arr = [5, 2, 8, 6, 1]
    rq = LinkedRangeQuery(arr, op=max, identity=float("-inf"))

    assert rq.range_query(0, 5) == 8
    assert rq.range_query(1, 4) == 8

    rq.update(2, -5)
    assert rq.range_query(0, 5) == 6

    # multiplication tests
    arr = [4, 6, 7]
    rq = LinkedRangeQuery(arr, op=lambda a, b: a * b, identity=1)

    assert rq.range_query(0, 3) == 168, f"{rq.range_query(0, 3)}"
    assert rq.range_query(1, 3) == 42, f"{rq.range_query(1, 3)}"
    assert rq.range_query(2, 3) == 7


    print("All tests passed!")