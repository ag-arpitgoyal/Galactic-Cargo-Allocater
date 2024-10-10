from avl import *
from object import Object

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects_tree = AVLTree(compare_object_ids)

    def add_object(self, object):
        self.objects_tree.insert(object.object_id, object)
        self.capacity -= object.size

    def remove_object(self, object_id):
        obj_node = self.objects_tree.find(self.objects_tree.root, object_id)
        self.capacity += obj_node.value.size
        self.objects_tree.delete(self.objects_tree.root, object_id)

    def objects_list(self):
        mylist = []
        root = self.objects_tree.root
        self.inorder(root, mylist)
        return mylist

    def inorder(self, root, mylist):
        if not root:
            return
        self.inorder(root.left, mylist)
        mylist.append(root.key)
        self.inorder(root.right, mylist)