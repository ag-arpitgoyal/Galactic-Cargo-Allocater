Galactic Cargo Management System (GCMS)
Overview
The Galactic Cargo Management System (GCMS) is a logistics management tool designed to efficiently handle and organize cargo in a galaxy-wide shipping network. This system employs advanced data structures, including AVL trees, to track and manage cargo bins, objects, and their capacities. The system supports efficient insertion, deletion, and searching of cargo based on various attributes like bin capacity, object size, and cargo color.

Features
Efficient Cargo Storage: AVL trees are used to manage and balance bin and object data, ensuring quick lookups and modifications.
Multi-Level Organization:
Bins are categorized by their capacities and IDs.
Objects are categorized by size and associated bins.
Color-Based Search: The system allows searching for bins based on their color, making retrieval fast and intuitive.
Fast Object Assignment: New objects are dynamically assigned to the best available bin based on current capacity.
Easy Object Management: Objects can be added or removed from bins with minimal computational overhead, ensuring scalable cargo management.
Data Structures
The GCMS uses three AVL trees for managing the cargo:

Bin Tree: Keys are tuples (capacity, bin_id) and values are bin instances. This AVL tree helps in organizing and retrieving bins based on their capacity and ID.

Object Tree: Keys are object_id and values are tuples (bin_instance, object_size). This AVL tree tracks the objects and their respective bin locations.

Bin-ID Tree: Keys are bin_id and values are bin instances. This tree allows quick access to bins using their unique IDs.

Class Structure
Bin Class: Contains attributes such as capacity, bin_id, and an AVL tree of objects that stores the sizes of objects in the bin.

Object Class: Holds information about the object such as object_id, size, and its associated bin.

GCMS Core Logic: The main system logic handles bin and object allocation, searches based on color, and capacity management.