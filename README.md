# Document Management System - CLI Version

A command-line implementation of a Document Management System, built in Python as a backup of my Data Structures and Algorithms (DSA) semester output. It manages 500 dynamically generated document records using custom-built data structures and algorithms, without relying on Python's built-in sorting or specialized containers for the core logic. The web version of this project was built with Streamlit; this CLI version runs the same core logic in any Python environment.

## Features

The program presents an interactive menu with 11 options:

1. **View All Documents** - displays the total number of active documents and lists the first 20.
2. **Search Document by ID** - retrieves a document by its ID (e.g., `DOC-0001`) using the hash table.
3. **Sort Documents** - sorts active documents by Name, Size, or Date using Merge Sort and shows the first 20.
4. **Edit a Document Name** - renames a document and saves the old name to its version history.
5. **View Version History of a Document** - shows the current name and all older versions, newest first.
6. **Browse Folders (Uses DFS)** - displays the folder tree and lists all documents under a chosen folder and its subfolders.
7. **Archive Document (Soft Delete)** - moves a document out of the active list without removing it.
8. **View Archived Documents** - lists all archived documents.
9. **Add New Document** - creates a document with an automatically assigned ID.
10. **Delete Document (Permanent)** - removes a document from both the hash table and the folder tree.
11. **Exit** - closes the program.

## Custom Data Structures Implemented

| Data Structure | Description |
|---|---|
| **VersionStack** | A custom LIFO (Last-In, First-Out) stack that stores the previous names of a document. Each edit pushes the old name onto the stack, so the newest older version is always on top. |
| **DocumentHashTable** | A custom hash table using **separate chaining** (a list of buckets, each holding a list of key-value pairs). It indexes documents by ID with a default capacity of 1009 buckets. Colliding keys share a bucket's chain. |
| **FolderTree** | A custom n-ary tree built from `FolderNode` objects. Each node stores its name, its child folders, and the IDs of the documents it contains. It models nested paths such as `Finance/Invoices`. |

## Custom Algorithms Implemented

- **Merge Sort** - a recursive divide-and-conquer algorithm that splits the document list in half, sorts each half, and merges them. It sorts by any document attribute (`name`, `size`, or `date`) and does not use Python's built-in `sort()` or `sorted()`.
- **Depth-First Search (DFS)** - a recursive traversal of the folder tree that collects the IDs of all documents located in a target folder and every one of its subfolders.

## How to Run

The program uses only the Python standard library (`random` and `datetime`), so no installation is required.

**Option A: Programiz (online)**
1. Open the Programiz online Python compiler.
2. Copy the entire contents of `document_management_system.py` and paste it into the editor.
3. Click **Run**.
4. Type your menu choice into the console panel and press Enter.

**Option B: Replit (online)**
1. Create a new Replit project and choose **Python** as the template.
2. Paste the code into `main.py` (or upload `document_management_system.py`).
3. Click **Run** and interact with the menu in the console.

**Option C: Local machine**
```bash
python document_management_system.py
```

**Notes:**
- On start-up, the program generates 500 random dummy documents, so the data differs on each run.
- Data is stored in memory only. Changes are not saved after the program exits.
- In option 6, enter a folder **name** (e.g., `Finance` or `Invoices`), not a full path.

## Complexity Analysis

Let **N** be the number of documents, **V** the number of folders, **E** the number of folder links, **P** the number of parts in a folder path, and **C** the number of children per folder.

| Component | Operation | Time Complexity | Space Complexity |
|---|---|---|---|
| VersionStack | push, pop, peek, is_empty | O(1) | O(1) per operation |
| VersionStack | get_all (full history) | O(K), K = versions | O(K) |
| DocumentHashTable | insert, search, remove | O(1) average, O(N) worst case | O(N) total |
| DocumentHashTable | get_all_active / get_all_archived | O(N) | O(N) |
| FolderTree | add_folder, add_document | O(P x C) | O(P) for new nodes |
| FolderTree | display_tree, remove_document_globally | O(V + D), D = documents stored | O(h), h = tree height |
| Merge Sort | sort by name, size, or date | O(N log N) in all cases | O(N) |
| DFS | folder search | O(V + E) | O(V) worst case (recursion stack) |

## Author

**Stephen Evangelista** - Individual Project
Data Structures and Algorithms (DSA) Semester Output
