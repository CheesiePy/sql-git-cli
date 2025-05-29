import os
import shutil
import subprocess
import sys
import sqlite3
from pathlib import Path

import pytest

# allow importing of our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.connection import connect_db

CLI = Path(__file__).parent.parent / "cli.py"

@pytest.fixture
def temp_repo(tmp_path, monkeypatch):
    """
    Create an isolated temp directory, cd into it, and yield it.
    Cleans up after the test finishes.
    """
    orig_cwd = Path.cwd()
    monkeypatch.chdir(tmp_path)
    # create a simple text file
    (tmp_path / "hello.txt").write_text("hello world\nsecond line")
    yield tmp_path
    # restore cwd and remove temp
    monkeypatch.chdir(orig_cwd)
    shutil.rmtree(tmp_path)

def run_cli(args, cwd):
    """Run `python3 cli.py <args>` in the given cwd, capture output."""
    proc = subprocess.run(
        [sys.executable, str(CLI)] + list(args),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc

def test_init_creates_git_dir(temp_repo):
    # first init
    proc = run_cli(["init"], temp_repo)
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert "Initialized empty git repository" in proc.stdout
    assert (temp_repo / ".sgit").is_dir()
    # init again should not error, but indicate already initialized
    proc2 = run_cli(["init"], temp_repo)
    assert proc2.returncode == 0
    assert "already initialized" in proc2.stdout.lower()

def test_add_commit_and_db_entries(temp_repo):
    # init repo
    run_cli(["init"], temp_repo)

    # stage single file
    proc = run_cli(["add", "hello.txt"], temp_repo)
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert "Staged: hello.txt" in proc.stdout

    # commit staged
    proc = run_cli(["commit", "first commit"], temp_repo)
    assert proc.returncode == 0
    assert proc.stderr == ""
    assert "Committed: first commit" in proc.stdout

    # inspect DB
    db_path = temp_repo / ".sgit" / "git.sqlite3"
    conn = connect_db(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM commits")
    assert cur.fetchone()[0] == 1

    cur.execute("SELECT COUNT(*) FROM code_lines")
    # two lines in hello.txt
    assert cur.fetchone()[0] == 2

def test_recursive_add_support(temp_repo):
    # init repo
    run_cli(["init"], temp_repo)

    # create nested structure
    nested_dir = temp_repo / "src" / "sub"
    nested_dir.mkdir(parents=True)
    (nested_dir / "a.txt").write_text("A\nB\nC")
    (nested_dir / "b.txt").write_text("X\nY")

    # add entire folder
    proc = run_cli(["add", "src"], temp_repo)
    assert proc.returncode == 0
    # should stage both files
    assert "Staged: src/sub/a.txt" in proc.stdout
    assert "Staged: src/sub/b.txt" in proc.stdout

    # commit them
    proc = run_cli(["commit", "add src"], temp_repo)
    assert "Committed: add src" in proc.stdout

    # verify code_lines count = 3 + 2 = 5
    db_path = temp_repo / ".sgit" / "git.sqlite3"
    conn = connect_db(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM code_lines")
    assert cur.fetchone()[0] == 5

def test_error_when_adding_nonexistent(temp_repo):
    run_cli(["init"], temp_repo)
    proc = run_cli(["add", "no_such_file.txt"], temp_repo)
    # Your CLI may throw an IOError or print an error message; adjust accordingly:
    assert proc.returncode != 0
    assert ("No such file" in proc.stderr) or ("Error" in proc.stderr)
