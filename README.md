# SQL-Git-CLI

A minimal Git-like version control system built with **Python** and **SQLite**, providing basic commands (`init`, `add`, `commit`, `branch`, `checkout`, `blame`) via a custom CLI.

---

## 🚀 Features

* **`git init`**: Initialize a new repository (creates `.git/` and SQLite DB)
* **`git add <file|folder>`**: Stage single files or recursively add entire directories
* **`git commit "<message>"`**: Commit staged changes with a message
* **`git branch <name>`**: Create a new branch pointing to the latest commit
* **`git checkout <branch|commit>`**: Switch working directory to a branch or commit
* **`git blame <branch|commit> <file>`**: Annotate each line of a file with the last commit that changed it

---

## 🛠️ Prerequisites

* Python 3.8+ (tested on 3.13)
* SQLite (bundled with Python)
* `pytest` (for running tests)

---

## ⚙️ Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/YourUsername/SQL-Git-CLI.git
   cd SQL-Git-CLI
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Linux/macOS
   # venv\Scripts\activate      # Windows PowerShell
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Create shell alias**
   Add to your `~/.bashrc` or `~/.zshrc`:

   ```bash
   alias git="python3 $(pwd)/cli.py"
   source ~/.bashrc
   ```

---

## 💡 Usage Examples

1. **Initialize repository**

   ```bash
   git init
   # Creates .git/ and initializes SQLite DB
   ```

2. **Stage files**

   ```bash
   git add file1.txt          # Single file
   git add src/               # Recursively stage all files in src/
   ```

3. **Commit changes**

   ```bash
   git commit "Initial commit"
   ```

4. **Branching**

   ```bash
   git branch feature-x
   ```

5. **Checkout**

   ```bash
   git checkout feature-x     # Switch to branch
   git checkout 2             # Switch to commit ID 2
   ```

6. **Blame**

   ```bash
   git blame main file1.txt   # Outputs file1.txt.blame.csv
   ```

---

## 🧪 Testing

Run the full test suite with `pytest`:

```bash
pytest tests/
```