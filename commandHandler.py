import os
from operationBtree import BTree

def create(index_file):
    """Create a new indew file and initialize a B-Tree."""
    if os.path.exitst(index_file):
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
        btree.insert(key, value)
        print(f"Key {key} has value {value} is inserted.")
    else:
        print("Indexed file need to be opended or create to procceed.")
        
