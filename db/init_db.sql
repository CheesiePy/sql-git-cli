-- Commits: every git commit
CREATE TABLE IF NOT EXISTS commits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message TEXT NOT NULL,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Branches: map a branch name to the latest commit
CREATE TABLE IF NOT EXISTS branches (
  name TEXT PRIMARY KEY,
  commit_id INTEGER NOT NULL,
  FOREIGN KEY (commit_id) REFERENCES commits(id)
);

-- Files: track each unique file path
CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  path TEXT NOT NULL UNIQUE
);

-- CodeLines: snapshot of a file at a commit, line-by-line
CREATE TABLE IF NOT EXISTS code_lines (
  commit_id   INTEGER NOT NULL,
  file_id     INTEGER NOT NULL,
  line_number INTEGER NOT NULL,
  text        TEXT NOT NULL,
  PRIMARY KEY(commit_id, file_id, line_number),
  FOREIGN KEY(commit_id) REFERENCES commits(id),
  FOREIGN KEY(file_id) REFERENCES files(id)
);

-- Staging area: files you’ve “git add”-ed but not yet committed
CREATE TABLE IF NOT EXISTS staging (
  file_id     INTEGER    NOT NULL,
  line_number INTEGER    NOT NULL,
  text        TEXT       NOT NULL,
  PRIMARY KEY (file_id, line_number),
  FOREIGN KEY (file_id) REFERENCES files(id)
);
