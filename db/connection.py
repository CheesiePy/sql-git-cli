import os
import sqlite3

GIT_DIR = ".git"
DB_NAME = "git.sqlite3"

def get_db_path():
    """
    Traverses upward from the current directory to find the .git folder
    and returns the path to the SQLite database inside it.
    """
    current = os.getcwd()
    while current != "/":
        git_path = os.path.join(current, GIT_DIR)
        if os.path.isdir(git_path):
            return os.path.join(git_path, DB_NAME)
        current = os.path.dirname(current)
    raise FileNotFoundError(".git directory not found")

def connect_db(db_path):
    """
    Connects to the SQLite database given a full path and enforces foreign keys.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
