import os
import sqlite3
import argparse

def insert_directory_structure(db_path, root_dir):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Traverse the directory structure
    for module in os.listdir(root_dir):
        if module.startswith('.'):
            continue

        module_path = os.path.join(root_dir, module)

        if os.path.isdir(module_path):
            for version in os.listdir(module_path):
                if version.startswith('.'):
                    continue

                version_path = os.path.join(module_path, version)

                if os.path.isfile(version_path):
                    # Check if the module-version pair already exists in the table
                    cursor.execute("SELECT 1 FROM MODULE WHERE MODULE = ? AND VERSION = ?", (module, version))
                    if not cursor.fetchone():
                        # Insert the module-version pair with GPU_ENABLED set to FALSE
                        cursor.execute("INSERT INTO MODULE (MODULE, VERSION, GPU_ENABLED) VALUES (?, ?, ?)",
                                       (module, version, False))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Insert directory structure into SQLite database.")
    parser.add_argument("db_path", help="Path to the SQLite database file.")
    parser.add_argument("root_dir", help="Root directory to traverse.")

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    insert_directory_structure(args.db_path, args.root_dir)

if __name__ == "__main__":
    main()

