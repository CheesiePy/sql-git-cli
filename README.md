# SQL-Git-CLI

A minimal Git-like version control system built with **Python** and **SQLite**, providing basic commands (`init`, `add`, `commit`, `branch`, `checkout`, `blame`) via a custom CLI.

---

## 🚀 Features

* **`sgit init`**: Initialize a new repository (creates `.sgit/` and SQLite DB)
* **`sgit add <file|folder>`**: Stage single files or recursively add entire directories
* **`sgit commit "<message>"`**: Commit staged changes with a message
* **`sgit branch <name>`**: Create a new branch pointing to the latest commit
* **`sgit checkout <branch|commit>`**: Switch working directory to a branch or commit
* **`sgit blame <branch|commit> <file>`**: Annotate each line of a file with the last commit that changed it

---

## 🛠️ Prerequisites

* Python 3.8+ (tested on 3.13)
* SQLite (bundled with Python)
* `pytest` (for running tests)

---

## ⚙️ Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/CheesiePy/SQL-Git-CLI.git
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
   alias sgit="$(pwd)/sgit.sh"
   source ~/.bashrc
   ```

---

## 💡 Usage Examples

1. **Initialize repository**

   ```bash
   sgit init
   # Creates .sgit/ and initializes SQLite DB
   ```

2. **Stage files**

   ```bash
   sgit add file1.txt          # Single file
   sgit add src/               # Recursively stage all files in src/
   ```

3. **Commit changes**

   ```bash
   sgit commit "Initial commit"
   ```

4. **Branching**

   ```bash
   sgit branch feature-x
   ```

5. **Checkout**

   ```bash
   sgit checkout feature-x     # Switch to branch
   sgit checkout 2             # Switch to commit ID 2
   ```

6. **Blame**

   ```bash
   sgit blame main file1.txt   # Outputs file1.txt.blame.csv
   ```

---

## 🧪 Testing

Run the full test suite with `pytest`:

```bash
pytest tests/
```
