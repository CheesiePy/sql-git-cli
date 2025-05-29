import os

def normalize_path(path):
    """Return a normalized relative path from the repo root."""
    return os.path.normpath(os.path.relpath(os.path.abspath(path), os.getcwd()))

def stage_file(conn, path):
    """
    Reads a file and stages its content line-by-line into the database.
    Skips binary or non-UTF-8 files gracefully.
    """
    norm_path = normalize_path(path)
    cur = conn.cursor()

    # Ensure file entry exists
    cur.execute("SELECT id FROM files WHERE path = ?", (norm_path,))
    row = cur.fetchone()
    if row:
        file_id = row[0]
    else:
        cur.execute("INSERT INTO files (path) VALUES (?)", (norm_path,))
        file_id = cur.lastrowid

    # Remove old staging entries for this file
    cur.execute("DELETE FROM staging WHERE file_id = ?", (file_id,))

    # Try reading file lines as UTF-8; skip on decode error or if inaccessible
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                cur.execute(
                    "INSERT INTO staging (file_id, line_number, text) VALUES (?, ?, ?)",
                    (file_id, i, line.rstrip("\n"))
                )
    except (UnicodeDecodeError, PermissionError, IsADirectoryError) as e:
        print(f"Skipping non-text or inaccessible file: {path}")

    conn.commit()
