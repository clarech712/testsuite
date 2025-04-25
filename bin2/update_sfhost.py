import sqlite3
import sys
import re

def get_module_versions(db_path, module_name):
    mn = "blast" if module_name == "blast_short" else module_name
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION FROM MODULE WHERE MODULE = ?", (mn,))
    versions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return versions

def rewrite_script(in_file, out_file, db, module):
    versions = get_module_versions(db, module)
    if not versions:
        raise ValueError(f"No versions found for module '{module}' in database.")

    with open(in_file, 'r') as f:
        lines = f.readlines()

    timestamp1 = timestamp2 = source_idx = None
    sfile = None

    for i, line in enumerate(lines):
        if 'timestamp' in line and timestamp1 is None:
            timestamp1 = i
        elif 'timestamp2' in line:
            timestamp2 = i
        elif 'source' in line and module in line:
            source_idx = i
            match = re.search(r'source\s+([^\s]+)', line)
            if match:
                sfile = match.group(1)

    if None in (timestamp1, timestamp2, source_idx, sfile):
        raise ValueError("Could not find required lines (timestamps/source) or module path in the input file.")

    header = lines[:timestamp1 + 1]
    body = lines[timestamp1 + 1:timestamp2]
    footer = lines[timestamp2:]

    with open(out_file, 'w') as out:
        # Write header
        out.writelines(header)

        # Begin for loop
        out.write(f"\nfor version in {' '.join(versions)}; do\n")
        out.write("  module purge 2>/dev/null\n")
        # out.write(f'  cat <(sed "s:{module}:{module}/$version:g" "{sfile}")\n\n')
        out.write(f'  source <(sed "s:{module}:{module}/$version:g" "{sfile}")\n\n')

        for i, line in enumerate(body):
            if i + timestamp1 + 1 == source_idx or "module purge" in line:
                continue
            out.write('  ' + line)

        out.write("done\n\n")

        # Write footer
        out.writelines(footer)

    print(f"Rewritten SLURM script with process substitution written to: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python update_sfhost.py <in_file> <out_file> <db> <module>")
        sys.exit(1)

    in_file, out_file, db, module = sys.argv[1:]
    versions = get_module_versions(db, module)
    
    if not versions:
        print(f"No versions found for module '{module}' in database.")
        sys.exit(0)  # You can use a special value like 0 for 'not found'

    rewrite_script(in_file, out_file, db, module)
    
    sys.exit(len(versions))  # Return number of versions as exit code

