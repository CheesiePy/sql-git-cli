#!/usr/bin/env python3

import os
import sys
from db.connection import get_db_path, connect_db
from utils.file_utils import stage_file

def init_repo():
    # Work in the current directory where the command was invoked
    working_dir = os.getcwd()
    print(f"DEBUG: init_repo running in: {working_dir}")  # you can remove this once verified

    # Create .git folder in that directory
    git_path = os.path.join(working_dir, ".sgit")
    if os.path.exists(git_path):
        print("Repository already initialized.")
        return
    os.makedirs(git_path)

    # Path to the SQLite file inside .git
    db_path = os.path.join(git_path, "git.sqlite3")

    # **Fix**: locate init_db.sql relative to this script’s directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(project_root, "db", "init_db.sql")

    with open(schema_path, "r") as f:
        conn = connect_db(db_path)
        conn.executescript(f.read())

    print("Initialized empty git repository in .git/")

def add_file(path):
    db_path = get_db_path()
    conn = connect_db(db_path)
    stage_file(conn, path)
    print(f"Staged: {path}")

def add_entry(path):
    """
    If `path` is a directory, recursively stage each file under it.
    Skips .git/, venv/, and __pycache__/, so you won’t try to read binaries.
    Otherwise, stage the single file.
    """
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            # don’t descend into these directories
            for skip in (".git", "venv", "__pycache__"):
                if skip in dirs:
                    dirs.remove(skip)

            for fname in files:
                full = os.path.join(root, fname)
                rel  = os.path.relpath(full, os.getcwd())
                conn = connect_db(get_db_path())
                stage_file(conn, rel)
                print(f"Staged: {rel}")
    else:
        add_file(path)

def commit_changes(message):
    db_path = get_db_path()
    conn = connect_db(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO commits (message) VALUES (?)", (message,))
    commit_id = cur.lastrowid

    cur.execute("""
        INSERT INTO code_lines (commit_id, file_id, line_number, text)
        SELECT ?, file_id, line_number, text FROM staging
    """, (commit_id,))
    cur.execute("DELETE FROM staging")
    conn.commit()
    print(f"Committed: {message}")

def create_branch(name):
    db_path = get_db_path()
    conn = connect_db(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM commits ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    if not result:
        print("No commits yet to branch from.")
        return
    commit_id = result[0]
    cur.execute("INSERT INTO branches (name, commit_id) VALUES (?, ?)", (name, commit_id))
    conn.commit()
    print(f"Branch '{name}' created at commit {commit_id}.")

def checkout(target):
    db_path = get_db_path()
    conn = connect_db(db_path)
    cur = conn.cursor()

    # Branch?
    cur.execute("SELECT commit_id FROM branches WHERE name = ?", (target,))
    row = cur.fetchone()
    commit_id = row[0] if row else None

    # Or direct commit
    if not commit_id:
        try:
            cid = int(target)
            cur.execute("SELECT id FROM commits WHERE id = ?", (cid,))
            row = cur.fetchone()
            commit_id = row[0] if row else None
        except ValueError:
            pass

    if not commit_id:
        print(f"Error: Branch or commit '{target}' not found.")
        return

    cur.execute("""
        SELECT f.path, c.line_number, c.text
        FROM code_lines c
        JOIN files f ON c.file_id = f.id
        WHERE c.commit_id = ?
        ORDER BY f.path, c.line_number
    """, (commit_id,))

    current_file = None
    buffer = []
    for path, ln, text in cur.fetchall():
        if path != current_file:
            if current_file:
                with open(current_file, "w") as outf:
                    outf.writelines(buffer)
            current_file = path
            buffer = []
        buffer.append(text + "\n")
    if current_file:
        with open(current_file, "w") as outf:
            outf.writelines(buffer)

    print(f"Checked out {target}.")

def blame(branch_or_commit, filename):
    db_path = get_db_path()
    conn = connect_db(db_path)
    cur = conn.cursor()

    # Resolve branch name
    cur.execute("SELECT commit_id FROM branches WHERE name = ?", (branch_or_commit,))
    row = cur.fetchone()
    commit_id = row[0] if row else None
    if not commit_id:
        try:
            commit_id = int(branch_or_commit)
        except ValueError:
            print(f"Invalid branch or commit: {branch_or_commit}")
            return

    # Find file
    cur.execute("SELECT id FROM files WHERE path = ?", (filename,))
    row = cur.fetchone()
    if not row:
        print(f"File '{filename}' not found.")
        return
    file_id = row[0]

    cur.execute("""
        SELECT cl.line_number, cl.text, cl.commit_id
        FROM code_lines cl
        WHERE cl.file_id = ? AND cl.commit_id <= ?
        GROUP BY cl.line_number
        ORDER BY cl.line_number
    """, (file_id, commit_id))

    out_name = filename + ".blame.csv"
    with open(out_name, "w") as outf:
        outf.write("line_number,text,last_commit_id\n")
        for ln, text, cid in cur.fetchall():
            outf.write(f"{ln},\"{text}\",{cid}\n")

    print(f"Blame written to {out_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: git <command> [args...]")
        return

    cmd, *args = sys.argv[1:]
    if cmd == "init":
        init_repo()
    elif cmd == "add":
        for p in args:
            add_entry(p)
    elif cmd == "commit":
        commit_changes(" ".join(args))
    elif cmd == "branch":
        create_branch(args[0])
    elif cmd == "checkout":
        checkout(args[0])
    elif cmd == "blame":
        blame(args[0], args[1])
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
