import os

def normalize_path(path):
    """Return a normalized absolute path (relative to project root)."""
    return os.path.relpath(os.path.abspath(path), os.getcwd())

def stage_file(conn, path):
    """
    Reads a file and inserts its lines into the staging table.
    If the file doesn't exist in the 'files' table, insert it.
    Replaces any previous staging entries for this file.
    """
    norm_path = normalize_path(path)
    
    cur = conn.cursor()

    # Get or insert file_id
    cur.execute("SELECT id FROM files WHERE path = ?", (norm_path,))
    row = cur.fetchone()
    if row:
        file_id = row[0]
    else:
        cur.execute("INSERT INTO files (path) VALUES (?)", (norm_path,))
        file_id = cur.lastrowid

    # Clear previous staging entries for the file
    cur.execute("DELETE FROM staging WHERE file_id = ?", (file_id,))

    # Read and stage new lines
    with open(path, "r") as f:
        for i, line in enumerate(f, start=1):
            cur.execute(
                "INSERT INTO staging (file_id, line_number, text) VALUES (?, ?, ?)",
                (file_id, i, line.rstrip('\n'))
            )

    conn.commit()


