from node import Node
from exceptions import *
from object import Color


def compare_capacity_and_bin_id(key1, key2):
    if key1[0] == key2[0]:
        return key1[1] - key2[1]  # Compare by capacity
    return key1[0] - key2[0]  # Compare by bin_id if capacities are equal


def compare_object_ids(key1, key2):
    return key1 - key2  # Compare object IDs (integers)


def compare_bin_ids(key1, key2):
    return key1 - key2  # Compare bin IDs (integers)


class AVLTree:
    def __init__(self, compare_function = compare_capacity_and_bin_id):
        self.root = None
        self.size = 0
        self.comparator = compare_function

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def balance_factor(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
            
    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def rotate_right(self, y):
        if not y.left:
            return y
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self.update_height(y)
        self.update_height(x)

        # Return the new root
        return x

    def rotate_left(self, x):
        if not x.right:
            return x
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self.update_height(x)
        self.update_height(y)

        # Return the new root
        return y

    def insert(self, root, key, value):
        if not root:
            return Node(key, value)

        # Use the custom comparator function to compare keys
        comparison = self.comparator(key, root.key)
        if comparison < 0:
            root.left = self.insert(root.left, key, value)
        elif comparison > 0:
            root.right = self.insert(root.right, key, value)
        else:
            # If the key already exists, update or handle as needed
            return root

        self.update_height(root)
        balance = self.balance_factor(root)

        # Balancing logic for AVL tree
        if balance > 1 and self.comparator(key, root.left.key) < 0:
            return self.rotate_right(root)
        if balance < -1 and self.comparator(key, root.right.key) > 0:
            return self.rotate_left(root)
        if balance > 1 and self.comparator(key, root.left.key) > 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and self.comparator(key, root.right.key) < 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root
    
    def delete(self, root, key):
        if root is None:
            return root

        comparison = self.comparator(key, root.key)
        
        if comparison < 0:
            root.left = self.delete(root.left, key)
        elif comparison > 0:
            root.right = self.delete(root.right, key)
        else:
            # Node with only one child or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node with two children: get the inorder successor (smallest in the right subtree)
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.value = temp.value  # Assuming you also want to update the value
            root.right = self.delete(root.right, temp.key)

        self.update_height(root)
        balance = self.balance_factor(root)

        # Balancing logic for AVL tree
        if balance > 1 and self.comparator(key, root.left.key) < 0:
            return self.rotate_right(root)
        if balance < -1 and self.comparator(key, root.right.key) > 0:
            return self.rotate_left(root)
        if balance > 1 and self.comparator(key, root.left.key) > 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and self.comparator(key, root.right.key) < 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root
        
    def search_by_key(self, root, key):
        """Finds and returns the node with the given key in the AVL tree."""
        if root is None:
            return None  # Key not found
        if self.comparator(key, root.key) == 0:
            return root  # Key found, return the node

        if self.comparator(key, root.key) < 0:
            return self.search_by_key(root.left, key)

        return self.search_by_key(root.right, key)
        
    def find_bin(self, osize, color):
        if self.root is None:
            raise NoBinFoundException
        if color == Color.BLUE:
            return self.blue_cargo(self.root, osize)
        elif color == Color.GREEN:
            return self.green_cargo(self.root, osize)
        elif color == Color.RED:
            node1 = self.green_cargo(self.root, osize)
            if node1 is None:
                raise NoBinFoundException
            capa = node1.key[0]
            return self.blue_cargo(self.root, capa)
        elif color == Color.YELLOW:
            node2 = self.blue_cargo(self.root, osize)
            if node2 is None:
                raise NoBinFoundException
            capa = node2.key[0]
            return self.yellow_cargo(self.root, capa)
        
    def blue_cargo(self, root, osize, s = None): 
        if not root:
            if s is None:
                raise NoBinFoundException
            return s
        if root.key[0] < osize:
            return self.blue_cargo(root.right, osize, s)
        if root.key[0] >= osize:
            if s is None or root.key[0] <= s.key[0]:
                s = root
            return self.blue_cargo(root.left, osize, s)
        
    def yellow_cargo(self, root, capa, s = None):
        if not root:
            return s
        if root.key[0] > capa:
            return self.yellow_cargo(root.left, capa, s)
        elif root.key[0] < capa:
            return self.yellow_cargo(root.right, capa, s)
        else:
            if s is None or s.key[1] < root.key[1]:
                s = root
            return self.yellow_cargo(root.right, capa, s)
        
    def green_cargo(self, root, osize, s = None):
        if not root:
            if s is None:
                raise NoBinFoundException
            return s
        if root.key[0] >= osize:
            if s is None or root.key[0] > s.key[0] or (root.key[0] == s.key[0] and root.key[1] > s.key[1]):
                s = root
        return self.green_cargo(root.right, osize, s)    
    
    def objects_list(self, b):
        lst = []
        root = b.objects_tree.root
        self.inorder(root, lst)
        return lst

    def inorder(self, root, lst):
        if not root:
            return
        self.inorder(root.left, lst)
        lst.append(root.key)
        self.inorder(root.right, lst)
    
    def pre_order(self, root):
        if not root:
            return
        print(root.key, end=" ")
        self.pre_order(root.left)
        self.pre_order(root.right)
        
        
