import sqlite3
import sys
import subprocess
import re

def get_partitions():
    """Retrieve a list of available partitions from Slurm."""
    try:
        result = subprocess.run(["scontrol", "show", "partitions"], capture_output=True, text=True, check=True)
        partitions = re.findall(r'PartitionName=(\S+)', result.stdout)
        return partitions
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving partitions: {e}")
        return []

def get_nodes_in_partition(partition):
    """Retrieve a list of nodes in a given partition."""
    try:
        result = subprocess.run(["sinfo", "-p", partition, "-N"], capture_output=True, text=True, check=True)
        nodes = re.findall(r'(\S+)\s+\d+', result.stdout)  # Extracts node names
        return nodes
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving nodes for partition {partition}: {e}")
        return []

def has_gpu(node):
    """Check if a given node has a GPU by parsing its Slurm info."""
    try:
        result = subprocess.run(["scontrol", "show", "node", node], capture_output=True, text=True, check=True)
        return bool(re.search(r'Gres=gpu(:\S+)?\b', result.stdout))  # Matches lines with GPU info
    except subprocess.CalledProcessError as e:
        print(f"Error checking GPU availability for node {node}: {e}")
        return False

def update_database(db_name):
    """Update the NODE table with any new (PARTITION, NODE) pairs."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        partitions = get_partitions()
        if not partitions:
            print("No partitions found. Exiting.")
            return
        
        for partition in partitions:
            nodes = get_nodes_in_partition(partition)
            for node in nodes:
                gpu_status = has_gpu(node)

                # Insert only if (PARTITION, NODE) does not already exist
                cursor.execute('''
                    INSERT INTO NODE (PARTITION, NODE, HAS_GPU)
                    SELECT ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM NODE WHERE PARTITION = ? AND NODE = ?
                    )
                ''', (partition, node, gpu_status, partition, node))

        conn.commit()
        print("Database successfully updated with new nodes.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_node.py <database_name>")
        sys.exit(1)

    db_name = sys.argv[1]
    update_database(db_name)

