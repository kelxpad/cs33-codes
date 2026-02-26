class RangeQuery:
    def __init__(self, data: list, op: callable, identity) -> None:
        self.n = len(data)
        self.op = op
        self.identity = identity

        # smallest power of two >= n
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        
        self.tree = [identity] * (2 * self.size)

        # build leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]

        # build internal nodes
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = op(self.tree[2*i], self.tree[2*i + 1])

    def update(self, index: int, value) -> None:
        pos = self.size + index
        self.tree[pos] = value

        pos //= 2
        while pos:
            self.tree[pos] = self.op(self.tree[2*pos], self.tree[2*pos+1])
            pos //= 2

    def range_query(self, left: int, right: int):
        res_left = self.identity
        res_right = self.identity

        left += self.size
        right += self.size

        while left < right:
            if left & 1:
                res_left = self.op(res_left, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                res_right = self.op(self.tree[right], res_right)

            left //= 2
            right //= 2

        return self.op(res_left, res_right)
    
if __name__ == "__main__":

    # test sums
    arr = [1, 3, 5, 7, 9]
    rq = RangeQuery(arr, op=lambda a, b: a + b, identity=0)

    assert rq.range_query(0, 5) == sum(arr)
    assert rq.range_query(1, 4) == 3 + 5 + 7
    assert rq.range_query(2, 3) == 5
    assert rq.range_query(0, 0) == 0  # empty range

    rq.update(2, 10)  # change 5 -> 10
    arr[2] = 10

    assert rq.range_query(0, 5) == sum(arr)
    assert rq.range_query(1, 4) == 3 + 10 + 7


    # min tests
    arr = [5, 2, 8, 6, 1]
    rq = RangeQuery(arr, op=min, identity=float("inf"))

    assert rq.range_query(0, 5) == 1
    assert rq.range_query(1, 4) == 2
    assert rq.range_query(4, 5) == 1

    rq.update(4, 100)
    assert rq.range_query(0, 5) == 2


    # max tests
    arr = [5, 2, 8, 6, 1]
    rq = RangeQuery(arr, op=max, identity=float("-inf"))

    assert rq.range_query(0, 5) == 8
    assert rq.range_query(1, 4) == 8

    rq.update(2, -5)
    assert rq.range_query(0, 5) == 6

    # multiplication tests
    arr = [4, 6, 7]
    rq = RangeQuery(arr, op=lambda a, b: a * b, identity=1)

    assert rq.range_query(0, 3) == 168, f"{rq.range_query(0, 3)}"
    assert rq.range_query(1, 3) == 42, f"{rq.range_query(1, 3)}"
    assert rq.range_query(2, 3) == 7


    print("All tests passed!")