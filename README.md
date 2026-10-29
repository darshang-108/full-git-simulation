# 🗂️ Task Tracker CLI — Full Gitflow Simulation

A minimal Python CLI application used to demonstrate a **complete Gitflow workflow** — including feature branches, pull requests, releases, hotfixes, merge-conflict resolution, and CI automation.

> **Goal:** Learn Git and GitHub workflows by building and shipping a real (tiny) project.

---

## Table of Contents

1. [Project Structure](#-project-structure)
2. [Quick Start](#-quick-start)
3. [Application Usage](#-application-usage)
4. [Full Gitflow Walkthrough](#-full-gitflow-walkthrough)
   - [Phase 0 — Initial Setup](#phase-0--initial-setup)
   - [Phase 1 — Feature Branch](#phase-1--feature-branch-featureadd-task)
   - [Phase 2 — Pull Request on GitHub](#phase-2--pull-request-on-github)
   - [Phase 3 — Release Branch](#phase-3--release-branch-release100)
   - [Phase 4 — Hotfix Branch](#phase-4--hotfix-branch-hotfix101)
5. [Merge Conflicts — Simulate & Resolve](#-merge-conflicts--simulate--resolve)
6. [Advanced Git Commands](#-advanced-git-commands)
   - [git rebase](#git-rebase)
   - [git stash](#git-stash)
   - [git cherry-pick](#git-cherry-pick)
7. [Pre-commit Hook](#-pre-commit-hook)
8. [GitHub Actions CI](#-github-actions-ci)
9. [Summary Cheat-Sheet](#-summary-cheat-sheet)

---

## 📁 Project Structure

```
task-tracker-cli/
├── .github/
│   └── workflows/
│       └── ci.yml              ← GitHub Actions CI pipeline
├── hooks/
│   └── pre-commit              ← Pre-commit hook script
├── task_tracker/
│   ├── __init__.py             ← Package init + version
│   ├── cli.py                  ← argparse-based CLI
│   └── storage.py              ← JSON file-based CRUD
├── tests/
│   ├── __init__.py
│   └── test_tracker.py         ← pytest test suite (14 tests)
├── .gitignore
├── requirements.txt
├── setup_hooks.py              ← Hook installer helper
└── README.md                   ← You are here
```

---

## 🚀 Quick Start

```bash
# 1. Clone or enter the project directory
cd "full git simulation"

# 2. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the tests
pytest -v

# 5. Try the CLI
python -m task_tracker.cli add "Learn Gitflow"
python -m task_tracker.cli list
python -m task_tracker.cli update 1 --status done
python -m task_tracker.cli delete 1
```

---

## 🖥️ Application Usage

| Command | Example |
|---------|---------|
| **Add** a task | `python -m task_tracker.cli add "Buy groceries"` |
| **List** all tasks | `python -m task_tracker.cli list` |
| **Update** title or status | `python -m task_tracker.cli update 1 --title "Buy vegetables" --status in-progress` |
| **Delete** a task | `python -m task_tracker.cli delete 1` |
| **Show version** | `python -m task_tracker.cli -v` |

Valid statuses: `pending` · `in-progress` · `done`

---

## 🌳 Full Gitflow Walkthrough

Below is the **exact sequence of Git commands** to reproduce the entire Gitflow lifecycle.  
Commands marked 🖥️ run in your terminal; steps marked 🌐 are performed on GitHub.

### Phase 0 — Initial Setup

```bash
# ── Initialise the repository ──────────────────────────────────
cd "full git simulation"
git init
git add .
git commit -m "chore: initial project scaffold

- Add Task Tracker CLI (add / list / update / delete)
- Add pytest test suite (14 tests)
- Add .gitignore, requirements.txt
- Add GitHub Actions CI workflow
- Add pre-commit hook"

# ── Push to GitHub ─────────────────────────────────────────────
#    First, create an EMPTY repo on GitHub (no README, no .gitignore).
#    Replace <USERNAME> with your GitHub username.

git remote add origin https://github.com/<USERNAME>/task-tracker-cli.git
git branch -M main
git push -u origin main

# ── Create the develop branch ──────────────────────────────────
git checkout -b develop
git push -u origin develop
```

**Verify:** You now have two branches on GitHub — `main` and `develop`.

---

### Phase 1 — Feature Branch (`feature/add-task`)

> Simulate adding the "add task" feature on a feature branch.

```bash
# ── Create the feature branch off develop ──────────────────────
git checkout develop
git checkout -b feature/add-task

# ── Make a change (example: improve the add_task docstring) ────
```

Open `task_tracker/storage.py` and add a detailed docstring to `add_task`:

```python
def add_task(title: str, filepath: str = DEFAULT_FILE) -> dict:
    """Create a new task and persist it.

    Args:
        title:    The task title (must not be empty).
        filepath: Path to the JSON storage file.

    Returns:
        The newly created task dict with keys id, title, status.

    Raises:
        ValueError: If title is empty or whitespace-only.
    """
```

```bash
# ── Commit the change ─────────────────────────────────────────
git add task_tracker/storage.py
git commit -m "feat: add detailed docstring to add_task function"

# ── Push the feature branch ────────────────────────────────────
git push -u origin feature/add-task
```

---

### Phase 2 — Pull Request on GitHub

🌐 **On GitHub:**

1. Navigate to your repository → **Pull requests** → **New pull request**.
2. Set **base:** `develop` ← **compare:** `feature/add-task`.
3. Title: `feat: add detailed docstring to add_task`.
4. Description:
   ```
   ## What
   Adds a comprehensive Google-style docstring to the `add_task` function.

   ## Testing
   - All 14 existing tests still pass (`pytest -v`).
   - No functional changes.
   ```
5. Click **Create pull request**.
6. Review the diff in the **Files changed** tab.
7. Click **Merge pull request** → **Confirm merge**.
8. Optionally delete the `feature/add-task` branch on GitHub.

🖥️ **Back in your terminal:**

```bash
# ── Sync local develop ────────────────────────────────────────
git checkout develop
git pull origin develop

# ── Clean up ───────────────────────────────────────────────────
git branch -d feature/add-task
```

---

### Phase 3 — Release Branch (`release/1.0.0`)

```bash
# ── Create the release branch off develop ──────────────────────
git checkout develop
git checkout -b release/1.0.0
```

Open `task_tracker/__init__.py` and set the version:

```python
__version__ = "1.0.0"
```

```bash
# ── Commit the version bump ───────────────────────────────────
git add task_tracker/__init__.py
git commit -m "chore: bump version to 1.0.0 for release"

# ── Run final tests ───────────────────────────────────────────
pytest -v          # All 14 tests must pass

# ── Push the release branch ───────────────────────────────────
git push -u origin release/1.0.0
```

🌐 **On GitHub — create two PRs:**

| PR | Base | Compare |
|----|------|---------|
| 1 | `main` | `release/1.0.0` |
| 2 | `develop` | `release/1.0.0` |

Merge **PR 1 into main first**, then **PR 2 into develop**.

🖥️ **Tag the release:**

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0 — initial stable release"
git push origin v1.0.0
```

🌐 **On GitHub:**  
Go to **Releases** → **Create a new release** → select tag `v1.0.0` → add notes → **Publish**.

```bash
# ── Clean up ───────────────────────────────────────────────────
git branch -d release/1.0.0
git checkout develop
git pull origin develop
```

---

### Phase 4 — Hotfix Branch (`hotfix/1.0.1`)

> Scenario: In production (`main`) we discover that `delete_task` doesn't return a confirmation message in the CLI.

```bash
# ── Create the hotfix branch off main ──────────────────────────
git checkout main
git checkout -b hotfix/1.0.1
```

Open `task_tracker/__init__.py` and bump the version:

```python
__version__ = "1.0.1"
```

Then open `task_tracker/cli.py` and find the delete block. It already prints a message, so let's add a small improvement — add a confirmation prompt before deleting. Replace the delete section in `main()` with:

```python
    elif args.command == "delete":
        try:
            # Show which task will be deleted before removing it
            from task_tracker.storage import list_tasks as _lt
            current = [t for t in _lt() if t["id"] == args.id]
            if current:
                print(f"Deleting: #{current[0]['id']} — {current[0]['title']}")
            task = delete_task(args.id)
            print(f"🗑️  Deleted task #{task['id']}: {task['title']}")
        except KeyError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
```

```bash
# ── Commit the hotfix ─────────────────────────────────────────
git add -A
git commit -m "fix: show task info before deletion, bump to 1.0.1"

# ── Push the hotfix branch ─────────────────────────────────────
git push -u origin hotfix/1.0.1
```

🌐 **On GitHub — create two PRs:**

| PR | Base | Compare |
|----|------|---------|
| 1 | `main` | `hotfix/1.0.1` |
| 2 | `develop` | `hotfix/1.0.1` |

Merge both PRs.

🖥️ **Tag the hotfix:**

```bash
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix v1.0.1 — show task info before deletion"
git push origin v1.0.1

# ── Clean up ───────────────────────────────────────────────────
git branch -d hotfix/1.0.1
git checkout develop
git pull origin develop
```

---

## 💥 Merge Conflicts — Simulate & Resolve

This section walks through creating and resolving a real merge conflict.

### Step 1 — Create two branches that edit the same line

```bash
git checkout develop

# ── Branch A ───────────────────────────────────────────────────
git checkout -b conflict/branch-a
```

Edit `task_tracker/storage.py` — change the `DEFAULT_FILE` constant:

```python
DEFAULT_FILE = "data/tasks_a.json"
```

```bash
git add task_tracker/storage.py
git commit -m "branch-a: change default file path"
git checkout develop

# ── Branch B ───────────────────────────────────────────────────
git checkout -b conflict/branch-b
```

Edit the same line in `task_tracker/storage.py`:

```python
DEFAULT_FILE = "data/tasks_b.json"
```

```bash
git add task_tracker/storage.py
git commit -m "branch-b: change default file path"
```

### Step 2 — Merge A into develop, then attempt to merge B

```bash
git checkout develop
git merge conflict/branch-a          # Succeeds — no conflict

git merge conflict/branch-b          # ⚠️ CONFLICT!
```

You'll see:

```
Auto-merging task_tracker/storage.py
CONFLICT (content): Merge conflict in task_tracker/storage.py
Automatic merge failed; fix conflicts and then commit the result.
```

### Step 3 — Resolve the conflict

Open `task_tracker/storage.py`. You'll find:

```
<<<<<<< HEAD
DEFAULT_FILE = "data/tasks_a.json"
=======
DEFAULT_FILE = "data/tasks_b.json"
>>>>>>> conflict/branch-b
```

Choose the correct value (or combine them). For example, revert to the original:

```python
DEFAULT_FILE = "tasks.json"
```

```bash
git add task_tracker/storage.py
git commit -m "resolve: merge conflict in DEFAULT_FILE — keep original"
```

### Step 4 — Clean up

```bash
git branch -d conflict/branch-a
git branch -d conflict/branch-b
```

---

## 🔧 Advanced Git Commands

### `git rebase`

Rebase replays your branch's commits on top of another branch, creating a linear history.

```bash
# ── Example: rebase a feature branch onto the latest develop ──
git checkout feature/my-feature
git rebase develop

# If conflicts arise during rebase:
# 1. Fix the conflict in the file
# 2. git add <file>
# 3. git rebase --continue
#
# To abort:  git rebase --abort
```

**When to use:** Before merging a feature branch, to keep the history clean.  
**When to avoid:** On shared/public branches — rebase rewrites commit hashes.

### `git stash`

Stash saves uncommitted changes so you can switch branches cleanly.

```bash
# ── Save current work ─────────────────────────────────────────
git stash push -m "WIP: halfway through update feature"

# ── Switch to another branch, do some work, come back ─────────
git checkout main
# ... do something ...
git checkout develop

# ── Restore stashed changes ───────────────────────────────────
git stash pop               # Applies and removes the top stash

# ── Other useful stash commands ────────────────────────────────
git stash list              # View all stashes
git stash apply stash@{0}   # Apply without removing
git stash drop stash@{0}    # Remove a specific stash
```

### `git cherry-pick`

Cherry-pick copies a single commit from one branch onto another.

```bash
# ── Find the commit hash you want ─────────────────────────────
git log --oneline develop    # e.g. abc1234 feat: add search

# ── Apply that one commit to main ──────────────────────────────
git checkout main
git cherry-pick abc1234

# If there's a conflict:
# 1. Resolve it
# 2. git add <file>
# 3. git cherry-pick --continue
```

**Use case:** A critical fix was committed to `develop` and you need it on `main` immediately without merging the entire branch.

---

## 🔒 Pre-commit Hook

The hook in `hooks/pre-commit` runs **Python syntax checks** and **pytest** before every commit. If either check fails, the commit is blocked.

### Installation

```bash
# Option A — use the helper script
python setup_hooks.py

# Option B — manual copy
cp hooks/pre-commit .git/hooks/pre-commit
# On Git Bash / Linux / macOS:
chmod +x .git/hooks/pre-commit
```

### Demo: hook blocks a bad commit

```bash
# Introduce a syntax error on purpose
echo "def broken(" >> task_tracker/storage.py

git add task_tracker/storage.py
git commit -m "this will fail"
# Output:
#   🔍 Running pre-commit checks...
#     ▸ Checking Python syntax...
#   ❌ Syntax error in task_tracker/storage.py — commit aborted.

# Fix it
git checkout -- task_tracker/storage.py
```

### Demo: hook blocks failing tests

```bash
# Break a function
# (change "pending" to "broken" in storage.py → add_task)
git add task_tracker/storage.py
git commit -m "this will also fail"
# Output:
#   🔍 Running pre-commit checks...
#     ✅ Syntax OK
#     ▸ Running pytest...
#   ❌ Tests failed — commit aborted.

# Revert
git checkout -- task_tracker/storage.py
```

---

## ⚙️ GitHub Actions CI

The workflow at `.github/workflows/ci.yml` triggers on every push and pull request to `main` and `develop`.

### What it does

1. Checks out the code.
2. Sets up Python 3.11 and 3.12 (matrix build).
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest -v`.

### Verify on GitHub

After pushing any branch:

1. Go to your repo → **Actions** tab.
2. You should see the workflow **"CI — Task Tracker"** running.
3. Click into it to see the test output for each Python version.

If tests pass you'll see a ✅ green check next to the commit on GitHub.

---

## 📋 Summary Cheat-Sheet

| Gitflow Step | Branch | Merges Into | Tag |
|---|---|---|---|
| Initial commit | `main` | — | — |
| Ongoing development | `develop` | — | — |
| New feature | `feature/add-task` | `develop` (via PR) | — |
| Release prep | `release/1.0.0` | `main` + `develop` | `v1.0.0` |
| Production bugfix | `hotfix/1.0.1` | `main` + `develop` | `v1.0.1` |

### Key commands at a glance

```bash
git checkout -b feature/X develop     # Start a feature
git checkout -b release/X.Y.Z develop # Start a release
git checkout -b hotfix/X.Y.Z main     # Start a hotfix
git tag -a vX.Y.Z -m "message"        # Tag a release
git merge --no-ff branch-name         # Merge preserving history
git rebase develop                    # Rebase onto develop
git stash push -m "message"           # Stash work-in-progress
git cherry-pick <commit-hash>         # Copy a single commit
```

---

## 📜 License

This project is provided as a learning exercise. Use it however you like.
