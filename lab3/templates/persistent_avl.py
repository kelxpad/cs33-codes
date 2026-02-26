class AVLNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.height = 1 + max(self.h(left), self.h(right))

    def h(self, node) -> int:
        return node.height if node else 0
    
class PersistentAVL:
    def __init__(self):
        self.versions = [None] # version 0 = empty tree

    def height(self, node):
        return node.height if node else 0
    
    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right)
    
    def rotate_right(self, y):
        x = y.left
        t2 = x.right

        new_y = AVLNode(y.key, t2, y.right)
        return AVLNode(x.key, x.left, new_y)
    
    def rotate_left(self, x):
        y = x.right
        t2 = y.left

        new_x = AVLNode(x.key, x.left, t2)
        return AVLNode(y.key, new_x, y.right)
    
    def balance(self, node):
        bf = self.balance_factor(node)

        # left heavy
        if bf > 1:
            if self.balance_factor(node.left) < 0:
                left_rotated = self.rotate_left(node.left)
                node = AVLNode(node.key, left_rotated, node.right)
            return self.rotate_right(node)
        
        # right heavy
        if bf < -1:
            if self.balance_factor(node.right) > 0:
                right_rotated = self.rotate_right(node.right)
                node = AVLNode(node.key, node.left, right_rotated)
            return self.rotate_left(node)
        
        return node
    
    def persistent_insert(self, node, key):
        if node is None:
            return AVLNode(key)
        
        if key < node.key:
            new_left = self.persistent_insert(node.left, key)
            new_node = AVLNode(node.key, new_left, node.right)
        elif key > node.key:
            new_right = self.persistent_insert(node.right, key)
            new_node = AVLNode(node.key, node.left, new_right)
        else:
            return node # no duplicates
        
        return self.balance(new_node)
    
    def insert(self, key, version=None):
        """insert key into a chosen version, returns new version index"""
        if version is None:
            version = len(self.versions) - 1
        
        new_root = self.persistent_insert(self.versions[version], key)
        self.versions.append(new_root)
        return len(self.versions) - 1
    
    def search(self, key, version=None):
        if version is None:
            version = len(self.versions) - 1

        node = self.versions[version]

        while node:
            if key == node.key:
                return True
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return False # not found

    def inorder(self, version=None):
        if version is None:
            version = len(self.versions) - 1
        
        result = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            result.append(node.key)
            dfs(node.right)
        
        dfs(self.versions[version])
        return result

tree = PersistentAVL()

v1 = tree.insert(10)   # version 1
v2 = tree.insert(5)    # version 2
v3 = tree.insert(15)   # version 3
v4 = tree.insert(7)    # version 4

print(tree.inorder(v2))  # [5, 10]
print(tree.inorder(v4))  # [5, 7, 10, 15]

print(tree.search(7, v2))  # False
print(tree.search(7, v4))  # True