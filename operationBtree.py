MAX_KEYS = 19
MAX_CHILDREN = 20
BLOCK_SIZE = 512

class Node:
    def __init__(self, block_id, leaf=False):
        self.block_id = block_id
        self.keys = [None] * MAX_KEYS
        self.values = [None] * MAX_KEYS
        self.children = [None] * MAX_CHILDREN
        self.leaf = leaf
        self.num_keys = 0
        self.parent_id = 0

    def serialize(self):
        # Convert the Node to bytes
        data = self.block_id.to_bytes(8, 'big') + \
               self.parent_id.to_bytes(8, 'big') + \
               self.num_keys.to_bytes(8, 'big')
        for key in self.keys:
            data += (key.to_bytes(8, 'big') if key else b'\x00' * 8)
        for value in self.values:
            data += (value.to_bytes(8, 'big') if value else b'\x00' * 8)
        for child in self.children:
            data += (child.to_bytes(8, 'big') if child else b'\x00' * 8)
        return data.ljust(BLOCK_SIZE, b'\x00')

    @staticmethod
    def deserialize(data):
        # Convert bytes back into a Node
        block_id = int.from_bytes(data[:8], 'big')
        parent_id = int.from_bytes(data[8:16], 'big')
        num_keys = int.from_bytes(data[16:24], 'big')
        keys = [int.from_bytes(data[24+i*8:32+i*8], 'big') if data[24+i*8:32+i*8].strip(b'\x00') else None for i in range(MAX_KEYS)]
        values = [int.from_bytes(data[184+i*8:192+i*8], 'big') if data[184+i*8:192+i*8].strip(b'\x00') else None for i in range(MAX_KEYS)]
        children = [int.from_bytes(data[344+i*8:352+i*8], 'big') if data[344+i*8:352+i*8].strip(b'\x00') else None for i in range(MAX_CHILDREN)]
        node = Node(block_id, leaf=False)
        node.parent_id = parent_id
        node.num_keys = num_keys
        node.keys = keys
        node.values = values
        node.children = children
        return node

class BTree:
    def __init__(self, degree, file):
        self.root = None
        self.t = degree
        self.file = file
        self.next_block_id = 1
        self.initialize_file()

    def initialize_file(self):
        # Write the header block
        header = b"4337PRJ3".ljust(8, b'\x00') + \
                 (0).to_bytes(8, 'big') + \
                 (1).to_bytes(8, 'big')
        self.file.write(header.ljust(BLOCK_SIZE, b'\x00'))

    def read_node(self, block_id):
        # Read a node from the file
        self.file.seek(block_id * BLOCK_SIZE)
        data = self.file.read(BLOCK_SIZE)
        return Node.deserialize(data)

    def write_node(self, node):
        # Write a node to the file
        self.file.seek(node.block_id * BLOCK_SIZE)
        self.file.write(node.serialize())

    def insert(self, key, value):
        # Implement B-Tree insertion logic
        if not self.root:
            self.root = Node(self.next_block_id, leaf=True)
            self.next_block_id += 1
            self.root.keys[0] = key
            self.root.values[0] = value
            self.root.num_keys = 1
            self.write_node(self.root)
        else:
            if self.root.num_keys == MAX_KEYS:
                new_root = Node(self.next_block_id, leaf = False)
                self.next_block_id += 1
                new_root.children[0] = self.root.block_id
                self.split_child(new_root,0,self.root)
                self.root = new_root
                self.insert_non_full(self.root, key, value)
                self.write_node(self.root)
            else:
                self.insert_non_full(self.root, key, value)

    def split_child(self, parent, index, child):
        """Split a full child node into two child and update the parent when inserting new key"""
        new_node = Node(self.next_block_id, leaf=child.leaf)
        self.next_block_id +=1
        new_node.num_keys = MAX_KEYS // 2

        for j in range(MAX_KEYS //2):
            new_node.keys[j] = child.keys[j + MAX_KEYS // 2 + 1]
            new_node.values[j] = child.values[j + MAX_KEYS // 2 +1]

            if not child.leaf:
                for j in range(MAX_KEYS // 2 + 1):
                    new_node.children[j] = child.children[j + MAX_KEYS // 2 + 1]

            child.num_keys = MAX_KEYS // 2 
            for j in range(parent.num_keys, index, -1):
                parent.children[j + 1] = parent.children[j]
            parent.children[index + 1] = new_node.block_id

            for j in range(parent.num_keys, index, -1):
                parent.keys[j + 1] = parent.keys[j]
                parent.values[j + 1] = parent.values[j]
            
            parent.keys[index] = child.keys[MAX_KEYS // 2]
            parent.values[index] = child.values[MAX_KEYS // 2]
            parent.num_keys += 1

            self.write_node(child)
            self.write_node(new_node)
            self.write_node(parent)

    def insert_non_full(self, node, key, value):
        """Insert a key_value pair into a non-full node."""
        i = node.num_keys -1
        if node.leaf:
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
            node.num_keys += 1
            self.write_node(node)
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            child = self.read_node(node.children[i])
            if child.num_keys == MAX_KEYS:
                self.split_child(node< i, child)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(child, key, value)



    def search(self, key):
        # Implement B-Tree search logic
        if not self.root:
            return None
        return self.search_recursive(self.root, key)
    
    def search_recursive(self, node, key):
        """Helper function for search"""
        i = 0
        while i < node.num_keys and key > node.keys[i]:
            i += 1
        if i < node.num_keys and key == node.keys[i]:
            return node.values[i]
        
        if node.leaf:
            return None
        child = self.read_node(node.children[i])
        return self.search_recursive(child,key)
