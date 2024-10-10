from bin import Bin
from avl import *
from object import Object, Color
from node import Node
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        self.bin_capacity_and_id_tree = AVLTree(compare_capacity_and_bin_id)
        self.object_id_tree = AVLTree(compare_object_ids)
        self.bin_id_tree = AVLTree(compare_bin_ids)

    def add_bin(self, bin_id, capacity):
        b = Bin(bin_id,capacity)
        
        self.bin_capacity_and_id_tree.root = self.bin_capacity_and_id_tree.insert(self.bin_capacity_and_id_tree.root, (capacity, bin_id), b)
        self.bin_id_tree.root = self.bin_id_tree.insert(self.bin_id_tree.root, bin_id, b)

    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)
        
        try:
            node1 = self.bin_capacity_and_id_tree.find_bin(size, color)
            bin1 = node1.value
            if not bin1:
                raise NoBinFoundException()
            
            key_for_deletion = (bin1.capacity, bin1.bin_id)
            bin1.objects_tree.root = bin1.objects_tree.insert(bin1.objects_tree.root, object_id, obj)
            
            
            self.bin_capacity_and_id_tree.root = self.bin_capacity_and_id_tree.delete(self.bin_capacity_and_id_tree.root, key_for_deletion)
            
            bin1.capacity -= size
            
            self.bin_capacity_and_id_tree.root = self.bin_capacity_and_id_tree.insert(self.bin_capacity_and_id_tree.root, (bin1.capacity, bin1.bin_id), bin1)
            
            self.object_id_tree.root = self.object_id_tree.insert(self.object_id_tree.root, object_id, bin1)
        except:
            raise NoBinFoundException()

    def delete_object(self, object_id):
        node1 = self.object_id_tree.search_by_key(self.object_id_tree.root, object_id)
        bin1 = node1.value
        
        self.object_id_tree.root = self.object_id_tree.delete(self.object_id_tree.root, object_id)
        
        obj_node = bin1.objects_tree.search_by_key(bin1.objects_tree.root, object_id)
        obj = obj_node.value
        s = obj.size
        
        key_for_deletion = (bin1.capacity, bin1.bin_id)
        self.bin_capacity_and_id_tree.root = self.bin_capacity_and_id_tree.delete(self.bin_capacity_and_id_tree.root, key_for_deletion)
        
        bin1.capacity += s
        
        self.bin_capacity_and_id_tree.root = self.bin_capacity_and_id_tree.insert(self.bin_capacity_and_id_tree.root, (bin1.capacity, bin1.bin_id), bin1)
        bin1.objects_tree.root = bin1.objects_tree.delete(bin1.objects_tree.root, object_id)

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        node1 = self.object_id_tree.search_by_key(self.object_id_tree.root, object_id)
        bin1 = node1.value
        return bin1.bin_id
    
    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        node1 = self.bin_id_tree.search_by_key(self.bin_id_tree.root, bin_id)
        bin1 = node1.value
        mylist = bin1.objects_list()
        return (bin1.capacity, mylist)
    