# ==========================================
# DOCUMENT MANAGEMENT SYSTEM - CLI VERSION
# Combined Parts 1, 2, and 3
# ==========================================

import random
from datetime import datetime, timedelta

# ==========================================
# PART 1: CUSTOM DATA STRUCTURES
# ==========================================

class VersionStack:
    """Custom LIFO Stack for tracking document version history."""
    def __init__(self):
        self.stack = []
        
    def push(self, version_name):
        # Time Complexity: O(1) amortized
        self.stack.append(version_name)
        
    def pop(self):
        # Time Complexity: O(1)
        if not self.is_empty():
            return self.stack.pop()
        return None
        
    def peek(self):
        # Time Complexity: O(1)
        if not self.is_empty():
            return self.stack[-1]
        return None
        
    def is_empty(self):
        # Time Complexity: O(1)
        return len(self.stack) == 0
        
    def get_all(self):
        # Time Complexity: O(N) where N is number of versions
        return self.stack[::-1]  # newest to oldest


class Document:
    """Represents a single document in the system."""
    def __init__(self, doc_id, name, folder, size, date):
        self.doc_id = doc_id
        self.name = name
        self.folder = folder
        self.size = size  # in KB
        self.date = date  # YYYY-MM-DD
        self.is_archived = False
        self.version_history = VersionStack()
        
    def __str__(self):
        status = "[ARCHIVED] " if self.is_archived else ""
        return f"{status}ID: {self.doc_id: <8} | {self.name: <25} | Size: {self.size: <6}KB | Date: {self.date} | Folder: /{self.folder}"


class DocumentHashTable:
    """Custom Hash Table using Separate Chaining (list of lists)."""
    def __init__(self, capacity=1009):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        
    def _hash(self, doc_id):
        # Time Complexity: O(1)
        return hash(doc_id) % self.capacity
        
    def insert(self, doc_id, doc_data):
        # Time Complexity: O(1) average
        index = self._hash(doc_id)
        for i, (k, v) in enumerate(self.table[index]):
            if k == doc_id:
                self.table[index][i] = (doc_id, doc_data)
                return
        self.table[index].append((doc_id, doc_data))
        
    def search(self, doc_id):
        # Time Complexity: O(1) average
        index = self._hash(doc_id)
        for k, v in self.table[index]:
            if k == doc_id:
                return v
        return None
        
    def remove(self, doc_id):
        # Time Complexity: O(1) average
        index = self._hash(doc_id)
        for i, (k, v) in enumerate(self.table[index]):
            if k == doc_id:
                del self.table[index][i]
                return True
        return False
        
    def get_all_active(self):
        # Time Complexity: O(N)
        active_docs = []
        for bucket in self.table:
            for k, doc in bucket:
                if not doc.is_archived:
                    active_docs.append(doc)
        return active_docs
        
    def get_all_archived(self):
        # Time Complexity: O(N)
        archived_docs = []
        for bucket in self.table:
            for k, doc in bucket:
                if doc.is_archived:
                    archived_docs.append(doc)
        return archived_docs


class FolderNode:
    """Node for the custom FolderTree."""
    def __init__(self, name):
        self.name = name
        self.children = []  # List of FolderNodes
        self.documents = []  # List of doc_ids

class FolderTree:
    """Custom n-ary Tree structure for hierarchical folders."""
    def __init__(self):
        self.root = FolderNode("root")
        
    def add_folder(self, path):
        # Time Complexity: O(P * C)
        parts = [p for p in path.split("/") if p]
        current = self.root
        
        for part in parts:
            found = False
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    break
            if not found:
                new_node = FolderNode(part)
                current.children.append(new_node)
                current = new_node
        return current
        
    def add_document(self, folder_path, doc_id):
        # Time Complexity: O(P * C)
        node = self.add_folder(folder_path)
        if doc_id not in node.documents:
            node.documents.append(doc_id)
            
    def display_tree(self, node=None, level=0):
        # Time Complexity: O(N)
        if node is None:
            node = self.root
        print("  " * level + "📁 " + node.name + f" ({len(node.documents)} docs)")
        for child in node.children:
            self.display_tree(child, level + 1)
            
    def remove_document_globally(self, node, doc_id):
        # Time Complexity: O(N)
        if doc_id in node.documents:
            node.documents.remove(doc_id)
        for child in node.children:
            self.remove_document_globally(child, doc_id)


# ==========================================
# PART 2: CUSTOM ALGORITHMS
# ==========================================

def merge_sort(docs, key):
    """
    Recursively sorts a list of Document objects based on the provided key.
    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    if len(docs) <= 1:
        return docs
        
    mid = len(docs) // 2
    left_half = merge_sort(docs[:mid], key)
    right_half = merge_sort(docs[mid:], key)
    
    return _merge(left_half, right_half, key)

def _merge(left, right, key):
    """Helper function to merge two sorted halves."""
    sorted_list = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        val_left = getattr(left[i], key)
        val_right = getattr(right[j], key)
        
        if val_left <= val_right:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
            
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    
    return sorted_list


def dfs_search(node, target_folder, found_target=False):
    """
    Depth First Search to find all document IDs in a target folder and its subfolders.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    results = []
    
    is_target_path = found_target or (node.name == target_folder)
    
    if is_target_path:
        results.extend(node.documents)
        
    for child in node.children:
        results.extend(dfs_search(child, target_folder, is_target_path))
        
    return results


# ==========================================
# PART 3: DUMMY DATA (STRING IDs) & MAIN MENU
# ==========================================

def generate_dummy_data(hash_table, tree):
    """
    Dynamically generates 500 dummy documents with string IDs.
    """
    prefixes = ["Q1", "Q2", "Q3", "Annual", "Draft", "Final", "Confidential", "Internal"]
    types = ["Report", "Summary", "Invoice", "Contract", "Blueprint", "Strategy", "Memo"]
    extensions = [".pdf", ".docx", ".xlsx", ".pptx", ".txt"]
    
    folders = [
        "Finance/Invoices", "Finance/Reports", "Finance/Taxes",
        "Engineering/Designs", "Engineering/Specs", "Engineering/Logs",
        "HR/Policies", "HR/Onboarding", "HR/Benefits",
        "Legal/Contracts", "Legal/Compliance"
    ]
    
    base_date = datetime(2020, 1, 1)
    
    for i in range(1, 501):
        doc_id = f"DOC-{i:04d}"
        
        filename = f"{random.choice(prefixes)}_{random.choice(types)}{random.choice(extensions)}"
        folder = random.choice(folders)
        size = random.randint(10, 50000)
        
        random_days = random.randint(0, 1800)
        date = (base_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        
        new_doc = Document(doc_id, filename, folder, size, date)
        
        hash_table.insert(doc_id, new_doc)
        tree.add_document(folder, doc_id)


def main():
    # Initialize the custom data structures
    db = DocumentHashTable()
    folder_tree = FolderTree()
    
    print("Initializing system and generating data...")
    generate_dummy_data(db, folder_tree)
    print("Initialization complete! Loaded 500 dummy documents.\n")
    
    while True:
        print("\n" + "="*50)
        print("           DOCUMENT MANAGEMENT SYSTEM")
        print("="*50)
        print("[1] View All Documents (First 20 only)")
        print("[2] Search Document by ID")
        print("[3] Sort Documents (by Name, Size, or Date)")
        print("[4] Edit a Document Name")
        print("[5] View Version History of a Document")
        print("[6] Browse Folders (Uses DFS)")
        print("[7] Archive Document (Soft Delete)")
        print("[8] View Archived Documents")
        print("[9] Add New Document")
        print("[10] Delete Document (Permanent)")
        print("[11] Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-11): ").strip()
        
        try:
            if choice == '1':
                active_docs = db.get_all_active()
                print(f"\n--- Total Active Documents: {len(active_docs)} ---")
                print("Showing first 20:")
                for doc in active_docs[:20]:
                    print(doc)
                    
            elif choice == '2':
                doc_id = input("Enter Document ID (e.g., DOC-0001): ").strip().upper()
                doc = db.search(doc_id)
                if doc and not doc.is_archived:
                    print("\nDocument Found:")
                    print(doc)
                else:
                    print("\nDocument not found or it has been archived.")
                    
            elif choice == '3':
                print("\nSort by: [1] Name  [2] Size  [3] Date")
                sort_choice = input("Enter choice (1-3): ").strip()
                sort_keys = {'1': 'name', '2': 'size', '3': 'date'}
                
                if sort_choice in sort_keys:
                    active_docs = db.get_all_active()
                    key = sort_keys[sort_choice]
                    print(f"\nSorting by {key}... please wait.")
                    sorted_docs = merge_sort(active_docs, key)
                    
                    print(f"\n--- First 20 Documents Sorted by {key.capitalize()} ---")
                    for doc in sorted_docs[:20]:
                        print(doc)
                else:
                    print("\nInvalid sorting option.")
                    
            elif choice == '4':
                doc_id = input("Enter Document ID to edit (e.g., DOC-0001): ").strip().upper()
                doc = db.search(doc_id)
                if doc and not doc.is_archived:
                    print(f"\nCurrent Name: {doc.name}")
                    new_name = input("Enter new document name: ").strip()
                    if new_name:
                        doc.version_history.push(doc.name)
                        doc.name = new_name
                        print("\nName updated successfully! Old version saved to history.")
                    else:
                        print("\nName cannot be empty. Update cancelled.")
                else:
                    print("\nDocument not found or is archived.")
                    
            elif choice == '5':
                doc_id = input("Enter Document ID (e.g., DOC-0001): ").strip().upper()
                doc = db.search(doc_id)
                if doc:
                    if doc.version_history.is_empty():
                        print("\nNo version history exists for this document.")
                    else:
                        print(f"\n--- Version History for {doc_id} ---")
                        print(f"Current Version: {doc.name}")
                        history = doc.version_history.get_all()
                        for i, old_name in enumerate(history, 1):
                            print(f"Older Version {i}: {old_name}")
                else:
                    print("\nDocument not found.")
                    
            elif choice == '6':
                print("\n--- Current Folder Structure ---")
                folder_tree.display_tree()
                
                target = input("\nEnter exact folder name to browse (e.g., 'Finance', 'Invoices'): ").strip()
                if target:
                    doc_ids = dfs_search(folder_tree.root, target)
                    if doc_ids:
                        unique_ids = set(doc_ids)
                        print(f"\n--- Found {len(unique_ids)} Document(s) in/under '{target}' ---")
                        for d_id in unique_ids:
                            doc = db.search(d_id)
                            if doc and not doc.is_archived:
                                print(doc)
                    else:
                        print(f"\nNo documents found for folder '{target}'.")
                        
            elif choice == '7':
                doc_id = input("Enter Document ID to archive (e.g., DOC-0001): ").strip().upper()
                doc = db.search(doc_id)
                if doc and not doc.is_archived:
                    doc.is_archived = True
                    print(f"\nDocument {doc_id} archived successfully.")
                else:
                    print("\nDocument not found or is already archived.")
                    
            elif choice == '8':
                archived_docs = db.get_all_archived()
                print(f"\n--- Archived Documents ({len(archived_docs)}) ---")
                if not archived_docs:
                    print("No documents have been archived.")
                else:
                    for doc in archived_docs:
                        print(doc)
                        
            elif choice == '9':
                all_docs = db.get_all_active() + db.get_all_archived()
                if all_docs:
                    max_id_num = max(int(d.doc_id.split('-')[1]) for d in all_docs)
                else:
                    max_id_num = 0
                next_id = f"DOC-{(max_id_num + 1):04d}"
                
                name = input("Enter document name: ").strip()
                folder = input("Enter folder path (e.g., HR/Policies): ").strip()
                size = int(input("Enter size in KB (e.g., 500): ").strip())
                date = datetime.now().strftime("%Y-%m-%d")
                
                new_doc = Document(next_id, name, folder, size, date)
                db.insert(next_id, new_doc)
                folder_tree.add_document(folder, next_id)
                print(f"\nDocument created successfully with ID: {next_id}")
                
            elif choice == '10':
                doc_id = input("Enter Document ID to PERMANENTLY delete (e.g., DOC-0001): ").strip().upper()
                doc = db.search(doc_id)
                if doc:
                    removed_from_db = db.remove(doc_id)
                    folder_tree.remove_document_globally(folder_tree.root, doc_id)
                    if removed_from_db:
                        print(f"\nDocument {doc_id} permanently deleted from the system.")
                else:
                    print("\nDocument not found.")
                    
            elif choice == '11':
                print("\nExiting Document Management System. Goodbye!")
                break
                
            else:
                print("\nInvalid choice. Please select a number from 1 to 11.")
                
        except ValueError:
            print("\nInvalid input. Please ensure numeric fields (like Size) contain numbers only.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
