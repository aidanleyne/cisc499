from Vector import Vector

"""
Node Class for the kd-tree
"""
class Node:
    def __init__(self, vec, key):
        self.right = None
        self.left = None
        self.height = 1
        self.key = key
        self.vector = vec

class Tree:
    def __init__(self):
        self.root = None

    """
    Function to insert a new node into the tree
    Returns: None
    Requires: vec - vector object
    """
    def insert(self, vec):
        self.root = self._insert(self.root, vec)

    """
    Helper function for inserting a new node in the tree
    Returns: New node object placed in tree
    Requires:
        node - parent node for new node to be placed below
        vec - vector object of the new node
    """
    def _insert(self, node, vec):
        if node is None:
            return Node(vec, 0)
        
        #calculate the key for the current vector-node combination
        key = self._calc_key(node, vec)

        if key < node.key:
            node.left = self._insert(node.left, vec)
        else:
            node.right = self._insert(node.right, vec)

        #currently removing the balancing of the tree
            #it only complicates things for now
            #would need to recalculate all keys when node is added
        """
        #get height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        #get balance factor of the tree
        balance_factor = self._get_balance(node)

        #rebalance tree to the left
        if balance_factor > 1:
            if key < node.left.key:
                return self._right_rotate(node)
            else:
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
            
        #rebalance tree to the right
        if balance_factor < -1:
            if key > node.right.key:
                return self._left_rotate(node)
            else:
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)
        """

    """
    Helper method to left-rotate the AVL-Tree
    """
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    """
    Helper method to right-rotate the AVL-Tree
    """
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    """
    Helper method to get the height of the AVL-Tree
    """
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    """
    Returns the balance of the tree based on sub-heights
    """
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    """
    Lookups-up closest node in the tree given a vector
    """
    def lookup(self, vec):
        return self._lookup(self.root, vec)

    def _lookup(self, node, vec):
        #calculate the key for the current vector
        key = self._calc_key(node, vec)

        #check for empty node or match
        if not node or node.key == key:
            return node

        #out-of-bounds on left side 
        if key < node.key:
            return self._lookup(node.left, key)
        
        #out-of-bounds on right side
        if key > node.key:
            self._lookup(node.right, key)

        return node

    """
    Calulates the difference in vectors between new and old node
    Returns: the difference factor
    Requires:
        node - node compared to
        vec - vector being used and placed
    """
    def _calc_key(self, node, vec):
        diff = 0
        for i in range(len(self.vector.arr)):
            diff += abs(node.vector.arr[i] - vec.arr[i]) / abs(node.vector.arr[i] + vec.arr[i])
        return diff / 256

def main():
    pass

if __name__ == "__main__":
    main()
        