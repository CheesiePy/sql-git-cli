#!/usr/bin/env bash
# Git wrapper script for SQL-Git-CLI
# Place this file under scripts/git.sh and either:
# 1) source it in your shell: source /path/to/sql-git-cli/scripts/git.sh
# 2) symlink it as "git" in your PATH: ln -s /path/to/sql-git-cli/scripts/git.sh ~/bin/git

# Determine project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Execute the Python CLI with all passed arguments
exec python3 "$SCRIPT_DIR/cli.py" "$@"
