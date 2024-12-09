import os
from operationBtree import BTree

def create(index_file):
    """Create a new indew file and initialize a B-Tree."""
    if os.path.exists(index_file):
        overwrite = input("File already exists. Overite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print("Aborting creation.")
            return None
    with open(index_file, 'wb+') as f:
        btree = BTree(degree=10, file = f)
        print(f"The {index_file} has been overwirte")
        return btree
    
def open_file(index_file):
    """Open existing index file."""
    #check if the path exsit or not
    if not os.path.exists(index_file):
        print("File does not exit.")
        return None
    #if it is then do this:
    with open(index_file, 'rb+') as f:
        magic_number = f.read(8).decode('utf-8').strip()
        if magic_number != "4337PRJ3":
            print("Invalid index file.")
            return None
        print(f"You are now in the index file: {index_file}")
        f.seek(0)
        btree = BTree(degree=10, file=f)
        return btree
    
def insert(btree, key, value):
    """insert a key-value pari into the Btree"""
    if btree:
        if btree.search(key):
            btree.insert(key, value)
            print(f"Key {key} has value {value} is inserted.")
        else: 
            print("The key is already exist in the btree")
    else:
        print("Indexed file need to be opended or create to procceed.")
        
def search(btree, key):
    """Search for a key in the index file"""
    if btree:
        value = btree.search(key)
        if value is not None: 
            print(f"Key {key} found with value {value}")
        else:
            print(f"Key {key} not found")
    else:
        print(f"Please open or create an index file first")

def load(btree, file_name):
    """Load key-value pairs from a file and insert them into the btree."""
    if not os.path.exists(file_name):
        print("File does not exist.")
        return
    with open(file_name, 'r') as f:
        for line in f:
            try:
                key, value = map(int, line.strip().split(","))
                insert(btree,key, value)
            except ValueError:
                print(f"Invalid line in file: {line.strip()}. Skipping.")

def print_btree(btree):
    """Print all key-value pairs in the B-Tree."""
    if btree:
        print("Tree contents:")
        print_in_order(btree.root, btree)
    else:
        print("No index file is opne. Please open or create an index file first.")

def print_in_order(node, btree):
    """Helper function to traverse and print the tree in order."""
    if node:
        for i in range(node.num_keys):
            if not node.leaf:
                child = btree.read_node(node.children[i])
                print_in_order(child, btree)
            print(f"Key: {node.keys[i]}, value: {node.values[i]}")
        if not node.leaf:
            child = btree.read_node(node.children[node.num_keys])
            print_in_order(child, btree)

def extract(btree, save_file):
    """Save all key-value pairs in the BTree ot a file."""
    if os.path.exists(save_file):
        overwrite = input("File already exists. Overwrite?(yes/no)").strip().lower()
        if overwrite != "yes":
            print("Aborting extraction.")
            return
    with open(save_file, "w") as f:
        extract_in_order(btree.root, btree, f)

def extract_in_order(node, btree, file):
    """Helper function to traverse the tree and write data to a file"""
    if node:
        for i in range(node.num_keys):
            if not node.leaf:
                child = btree.read_node(node.children[i])
                extract_in_order(child, btree, file)
            file.write(f"{node.keys[i]},{node.values[i]} \n")
        if not node.leaf:
            child = btree.read_node(node.children[node.num_keys])
            extract_in_order(child, btree, file)