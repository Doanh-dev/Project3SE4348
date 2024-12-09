from commandHandler import create, open_file, insert, search, load, print_btree, extract

def display_menu():
    """Display the user menu"""
    print(f"\n_____________Menu______________\n")
    print("1. create: Create a new index file")
    print("2. open: Open an index file")
    print("3. insert: Insert key and value")
    print("4. search: Searching")
    print("5. load: loading a keys and values")
    print("6. print: Print BTree structure")
    print("7. extract: Extract the keys and values")
    print("8. quite: Quit the program \n")

def main():
    """Interactive menu"""
    btree = None
    while True:
        display_menu()
        command = input("Enter command: ").strip().lower()
        if command in {"1", "create"}:
            filename = input("Enter filename: ")
            btree = create(filename)
        elif command in {"2", "open"}:
            filename = input("Enter filename: ")
            btree = open_file(filename)
        elif command in {"3", "insert"}:
            if btree:
                key = int(input("Enter key: "))
                value = int(input("Enter value: "))
                insert(btree, key, value)
            else:
                print("No index file is open. Please create or open a new index file")
        elif command in {"4", "search"}:
            if btree: 
                key = int(input("Enter the key to search: "))
                search(btree, key)
            else:
                print("No Inde file is open, Please create or open a new index file. ")
        elif command in {"5", "load"}:
            if btree:
                filename = input("Enter the loading file: ")
                load(btree, filename)
        elif command in {"6", "print"}:
            if btree:
                print_btree(btree)
            else: 
                print("No Inde file is open, Please create or open a new index file. ")
        elif command in {"7", "extract"}:
            if btree:
                filename = input("Enter the file to save to: ")
                extract(btree, filename)
            else:
                print("No Inde file is open, Please create or open a new index file. ")
        elif command in {"8", "quit"}:
            print("You exits program")
            break
        else:
            print("Invalid command, please select from the menu")

if __name__ == "__main__":
    main()
