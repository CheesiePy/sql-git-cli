import os

def find_git_root(start_path=None):
    """
    Traverse upwards from start_path (or current dir) to find the nearest .git folder.
    Returns the path to the root project directory containing .git.
    Raises FileNotFoundError if not found.
    """
    current = os.path.abspath(start_path or os.getcwd())
    
    while current != os.path.dirname(current):  # until reaching root
        if os.path.isdir(os.path.join(current, ".sgit")):
            return current
        current = os.path.dirname(current)
    
    raise FileNotFoundError("No .git directory found in any parent folders.")
